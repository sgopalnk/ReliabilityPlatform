"""
Unit tests for the ChatOps Assistant.
"""

from unittest.mock import MagicMock

import pytest

from operations_center.chatops_assistant.src.exceptions import ChatOpsAssistantError
from operations_center.chatops_assistant.src.models import ChatResponse
from operations_center.chatops_assistant.src.services.chatops_assistant import (
    ChatOpsAssistant,
)


def test_answer_returns_chat_response():
    """
    Verify the ChatOps Assistant returns a ChatResponse object.
    """
    assistant = ChatOpsAssistant()

    assistant.llm_client.generate = MagicMock(
        return_value='{"answer":"MTTR is Mean Time To Recovery."}'
    )

    response = assistant.answer("What is MTTR?")

    assert isinstance(response, ChatResponse)
    assert response.answer == "MTTR is Mean Time To Recovery."

    assistant.llm_client.generate.assert_called_once()


def test_answer_raises_error_for_invalid_json():
    """
    Verify invalid JSON returned by the LLM raises ChatOpsAssistantError.
    """
    assistant = ChatOpsAssistant()

    assistant.llm_client.generate = MagicMock(
        return_value="This is not JSON"
    )

    with pytest.raises(ChatOpsAssistantError):
        assistant.answer("What is MTTR?")