"""Support ticket classification and routing workflow."""

import http
from typing import Literal

from pydantic import BaseModel

import mistralai.workflows as workflows
from mistralai.workflows.exceptions import ErrorCode, WorkflowsException

# Allowed values for classification
CategoryType = Literal["bug", "billing", "feature request", "other"]
PriorityType = Literal["low", "medium", "high", "urgent"]
TeamQueueType = Literal["engineering", "billing", "product", "support"]


class TicketInput(BaseModel):
    """Input for the ticket router workflow."""

    subject: str
    body: str


class RoutingDecision(BaseModel):
    """Output routing decision for a support ticket."""

    category: CategoryType
    priority: PriorityType
    team_queue: TeamQueueType
    reason: str


@workflows.activity(retry_policy_max_attempts=3)
async def classify_ticket(subject: str, body: str) -> RoutingDecision:
    """Classify a support ticket using a Mistral model.
    
    This activity calls the Mistral model to analyze the ticket and determine:
    - Category: bug, billing, feature request, or other
    - Priority: low, medium, high, or urgent
    - Team Queue: engineering, billing, product, or support
    - Reason: one-sentence explanation
    """
    import json
    import os
    
    # Import here to avoid sandbox restriction during module import
    from utils.mistral import mistral_client
    
    # Get Mistral client, using SERVER_URL if set (platform-injected)
    server_url = os.environ.get("SERVER_URL")
    client = mistral_client(server_url=server_url)
    
    prompt = f"""You are a support ticket classification and routing assistant.

Analyze the following support ticket and provide a structured routing decision.

**Ticket Subject:** {subject}
**Ticket Body:** {body}

**Classification Categories:**
- bug: Technical issue or software defect
- billing: Payment, subscription, or invoice related
- feature request: Request for new functionality
- other: Anything not fitting the above

**Priority Levels:**
- urgent: System down, critical business impact, security issue
- high: Major functionality broken, multiple users affected
- medium: Normal issue affecting workflow
- low: Minor issue, cosmetic, or enhancement

**Team Queues:**
- engineering: For bugs and technical issues
- billing: For billing and payment matters
- product: For feature requests and roadmap items
- support: For general inquiries and other requests

Respond with a JSON object containing exactly these fields:
{{
  "category": "bug|billing|feature request|other",
  "priority": "low|medium|high|urgent",
  "team_queue": "engineering|billing|product|support",
  "reason": "one-sentence explanation of the routing decision"
}}

Respond ONLY with the valid JSON object. Do not include any other text, markdown, or explanations."""

    response = await client.chat.complete_async(
        model="mistral-medium-latest",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        response_format={"type": "json_object"},
        temperature=0.0,
    )

    # Parse the JSON response
    message = response.choices[0].message
    content = message.content
    
    # Extract JSON from the response
    if content.startswith('```json'):
        content = content[7:].strip()
    if content.startswith('```'):
        content = content[3:].strip()
    
    # Find the first { and last }
    start = content.find('{')
    end = content.rfind('}') + 1
    if start >= 0 and end > start:
        json_str = content[start:end]
    else:
        json_str = content
    
    result = json.loads(json_str)
    
    return RoutingDecision(
        category=result["category"],
        priority=result["priority"],
        team_queue=result["team_queue"],
        reason=result["reason"],
    )


@workflows.workflow.define(
    name="mb-qa-ticket-router",
    workflow_display_name="MB QA Ticket Router",
    workflow_description="Route support tickets to appropriate teams with category and priority classification",
)
class TicketRouterWorkflow:
    @workflows.workflow.entrypoint
    async def run(self, input: TicketInput) -> RoutingDecision:
        """Route a support ticket by classifying it and determining the appropriate team."""
        # Validate input - raise WorkflowsException for non-retryable validation errors
        if not input.subject or not input.subject.strip():
            raise WorkflowsException(
                code=ErrorCode.INVALID_ARGUMENTS_ERROR,
                message="subject must not be empty or whitespace-only",
                status=http.HTTPStatus.BAD_REQUEST,
            )
        if not input.body or not input.body.strip():
            raise WorkflowsException(
                code=ErrorCode.INVALID_ARGUMENTS_ERROR,
                message="body must not be empty or whitespace-only",
                status=http.HTTPStatus.BAD_REQUEST,
            )
        return await classify_ticket(input.subject, input.body)
