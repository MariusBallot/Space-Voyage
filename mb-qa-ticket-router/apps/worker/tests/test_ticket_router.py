"""Unit tests for the ticket router workflow."""

import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from worker.workflows.ticket_router import (
    TicketInput,
    TicketRouterWorkflow,
    RoutingDecision,
    classify_ticket,
)


@pytest.mark.asyncio
async def test_classify_ticket_bug():
    """Test classification of a bug ticket."""
    # Mock the response from the Mistral model
    mock_message = MagicMock()
    mock_message.content = json.dumps({
        "category": "bug",
        "priority": "high",
        "team_queue": "engineering",
        "reason": "Login failure affects authentication"
    })
    
    mock_choice = MagicMock()
    mock_choice.message = mock_message
    
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    
    mock_client = MagicMock()
    mock_client.chat.complete = AsyncMock(return_value=mock_response)
    
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
    mock_message = MagicMock()
    mock_message.content = json.dumps({
        "category": "billing",
        "priority": "medium",
        "team_queue": "billing",
        "reason": "Invoice discrepancy"
    })
    
    mock_choice = MagicMock()
    mock_choice.message = mock_message
    
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    
    mock_client = MagicMock()
    mock_client.chat.complete = AsyncMock(return_value=mock_response)
    
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
    mock_message = MagicMock()
    mock_message.content = json.dumps({
        "category": "feature request",
        "priority": "low",
        "team_queue": "product",
        "reason": "UI enhancement request"
    })
    
    mock_choice = MagicMock()
    mock_choice.message = mock_message
    
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    
    mock_client = MagicMock()
    mock_client.chat.complete = AsyncMock(return_value=mock_response)
    
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
    mock_message = MagicMock()
    mock_message.content = json.dumps({
        "category": "other",
        "priority": "low",
        "team_queue": "support",
        "reason": "General support question"
    })
    
    mock_choice = MagicMock()
    mock_choice.message = mock_message
    
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    
    mock_client = MagicMock()
    mock_client.chat.complete = AsyncMock(return_value=mock_response)
    
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
    mock_message = MagicMock()
    mock_message.content = json.dumps({
        "category": "bug",
        "priority": "urgent",
        "team_queue": "engineering",
        "reason": "Security vulnerability"
    })
    
    mock_choice = MagicMock()
    mock_choice.message = mock_message
    
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    
    mock_client = MagicMock()
    mock_client.chat.complete = AsyncMock(return_value=mock_response)
    
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
    mock_message = MagicMock()
    # Response wrapped in markdown code blocks
    mock_message.content = '```json\n{"category": "bug", "priority": "high", "team_queue": "engineering", "reason": "Test"}\n```'
    
    mock_choice = MagicMock()
    mock_choice.message = mock_message
    
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    
    mock_client = MagicMock()
    mock_client.chat.complete = AsyncMock(return_value=mock_response)
    
    with patch('utils.mistral.mistral_client', return_value=mock_client):
        result = await classify_ticket(
            subject="Test",
            body="Test ticket"
        )
    
    assert result.category == "bug"
    assert result.priority == "high"


def test_ticket_input_validation():
    """Test that TicketInput validates correctly."""
    # Valid input
    input_data = TicketInput(subject="Test", body="Test body")
    assert input_data.subject == "Test"
    assert input_data.body == "Test body"
    
    # Missing fields should raise ValidationError
    with pytest.raises(Exception):  # Pydantic ValidationError
        TicketInput()


def test_routing_decision_model():
    """Test that RoutingDecision model works correctly."""
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
