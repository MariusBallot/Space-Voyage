"""Unit tests for the ticket router workflow."""

import http
import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from mistralai.workflows.exceptions import ErrorCode, WorkflowsException

from worker.workflows.ticket_router import (
    TicketInput,
    TicketRouterWorkflow,
    RoutingDecision,
    classify_ticket,
)


def _make_mock_client(response_content: str):
    """Helper to create a mock client with complete_async returning a response."""
    mock_message = MagicMock()
    mock_message.content = response_content
    
    mock_choice = MagicMock()
    mock_choice.message = mock_message
    
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    
    mock_client = MagicMock()
    mock_client.chat.complete_async = AsyncMock(return_value=mock_response)
    return mock_client


@pytest.mark.asyncio
async def test_classify_ticket_bug():
    """Test classification of a bug ticket."""
    mock_client = _make_mock_client(json.dumps({
        "category": "bug",
        "priority": "high",
        "team_queue": "engineering",
        "reason": "Login failure affects authentication"
    }))
    
    with patch('utils.mistral.mistral_client', return_value=mock_client):
        result = await classify_ticket(
            subject="Login not working",
            body="Users cannot login to the application"
        )
    
    assert isinstance(result, RoutingDecision)
    assert result.category == "bug"
    assert result.priority == "high"
    assert result.team_queue == "engineering"
    assert result.reason == "Login failure affects authentication"


@pytest.mark.asyncio
async def test_classify_ticket_billing():
    """Test classification of a billing ticket."""
    mock_client = _make_mock_client(json.dumps({
        "category": "billing",
        "priority": "medium",
        "team_queue": "billing",
        "reason": "Invoice discrepancy"
    }))
    
    with patch('utils.mistral.mistral_client', return_value=mock_client):
        result = await classify_ticket(
            subject="Invoice question",
            body="My invoice shows $500 but I only have 10 users"
        )
    
    assert result.category == "billing"
    assert result.priority == "medium"
    assert result.team_queue == "billing"


@pytest.mark.asyncio
async def test_classify_ticket_feature_request():
    """Test classification of a feature request ticket."""
    mock_client = _make_mock_client(json.dumps({
        "category": "feature request",
        "priority": "low",
        "team_queue": "product",
        "reason": "UI enhancement request"
    }))
    
    with patch('utils.mistral.mistral_client', return_value=mock_client):
        result = await classify_ticket(
            subject="Dark mode request",
            body="Please add dark mode to the dashboard"
        )
    
    assert result.category == "feature request"
    assert result.priority == "low"
    assert result.team_queue == "product"


@pytest.mark.asyncio
async def test_classify_ticket_other():
    """Test classification of an other ticket."""
    mock_client = _make_mock_client(json.dumps({
        "category": "other",
        "priority": "low",
        "team_queue": "support",
        "reason": "General support question"
    }))
    
    with patch('utils.mistral.mistral_client', return_value=mock_client):
        result = await classify_ticket(
            subject="How to reset password",
            body="I forgot my password"
        )
    
    assert result.category == "other"
    assert result.priority == "low"
    assert result.team_queue == "support"


@pytest.mark.asyncio
async def test_classify_ticket_urgent():
    """Test classification of an urgent ticket."""
    mock_client = _make_mock_client(json.dumps({
        "category": "bug",
        "priority": "urgent",
        "team_queue": "engineering",
        "reason": "Security vulnerability"
    }))
    
    with patch('utils.mistral.mistral_client', return_value=mock_client):
        result = await classify_ticket(
            subject="Security issue",
            body="Potential SQL injection vulnerability"
        )
    
    assert result.category == "bug"
    assert result.priority == "urgent"


@pytest.mark.asyncio
async def test_classify_ticket_with_markdown():
    """Test classification when response has markdown code blocks."""
    mock_client = _make_mock_client(
        '```json\n{"category": "bug", "priority": "high", "team_queue": "engineering", "reason": "Test"}\n```'
    )
    
    with patch('utils.mistral.mistral_client', return_value=mock_client):
        result = await classify_ticket(
            subject="Test",
            body="Test ticket"
        )
    
    assert result.category == "bug"
    assert result.priority == "high"


def test_ticket_input_validation_valid():
    """Test that TicketInput accepts valid inputs."""
    input_data = TicketInput(subject="Test", body="Test body")
    assert input_data.subject == "Test"
    assert input_data.body == "Test body"


@pytest.mark.asyncio
async def test_workflow_validation_empty_subject():
    """Test that workflow rejects empty subject with WorkflowsException."""
    workflow = TicketRouterWorkflow()
    with pytest.raises(WorkflowsException) as exc_info:
        await workflow.run(TicketInput(subject="", body="Test body"))
    assert exc_info.value.code == ErrorCode.INVALID_ARGUMENTS_ERROR
    assert exc_info.value.status == http.HTTPStatus.BAD_REQUEST
    assert "subject must not be empty or whitespace-only" in exc_info.value.message


@pytest.mark.asyncio
async def test_workflow_validation_empty_body():
    """Test that workflow rejects empty body with WorkflowsException."""
    workflow = TicketRouterWorkflow()
    with pytest.raises(WorkflowsException) as exc_info:
        await workflow.run(TicketInput(subject="Test", body=""))
    assert exc_info.value.code == ErrorCode.INVALID_ARGUMENTS_ERROR
    assert exc_info.value.status == http.HTTPStatus.BAD_REQUEST
    assert "body must not be empty or whitespace-only" in exc_info.value.message


@pytest.mark.asyncio
async def test_workflow_validation_whitespace_only():
    """Test that workflow rejects whitespace-only inputs with WorkflowsException."""
    workflow = TicketRouterWorkflow()
    with pytest.raises(WorkflowsException) as exc_info:
        await workflow.run(TicketInput(subject="   ", body="   "))
    assert exc_info.value.code == ErrorCode.INVALID_ARGUMENTS_ERROR
    assert exc_info.value.status == http.HTTPStatus.BAD_REQUEST
    assert "subject must not be empty or whitespace-only" in exc_info.value.message


@pytest.mark.asyncio
async def test_workflow_validation_both_empty():
    """Test that workflow rejects both empty with WorkflowsException."""
    workflow = TicketRouterWorkflow()
    with pytest.raises(WorkflowsException) as exc_info:
        await workflow.run(TicketInput(subject="", body=""))
    assert exc_info.value.code == ErrorCode.INVALID_ARGUMENTS_ERROR
    assert exc_info.value.status == http.HTTPStatus.BAD_REQUEST
    assert "subject must not be empty or whitespace-only" in exc_info.value.message


def test_routing_decision_model_valid():
    """Test that RoutingDecision accepts valid values."""
    decision = RoutingDecision(
        category="bug",
        priority="high",
        team_queue="engineering",
        reason="Test reason"
    )
    assert decision.category == "bug"
    assert decision.priority == "high"
    assert decision.team_queue == "engineering"
    assert decision.reason == "Test reason"


def test_routing_decision_model_invalid_category():
    """Test that RoutingDecision rejects invalid category."""
    with pytest.raises(ValueError):
        RoutingDecision(
            category="invalid",
            priority="high",
            team_queue="engineering",
            reason="Test"
        )


def test_routing_decision_model_invalid_priority():
    """Test that RoutingDecision rejects invalid priority."""
    with pytest.raises(ValueError):
        RoutingDecision(
            category="bug",
            priority="invalid",
            team_queue="engineering",
            reason="Test"
        )


def test_routing_decision_model_invalid_team_queue():
    """Test that RoutingDecision rejects invalid team_queue."""
    with pytest.raises(ValueError):
        RoutingDecision(
            category="bug",
            priority="high",
            team_queue="invalid",
            reason="Test"
        )
