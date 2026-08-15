from unittest.mock import MagicMock

from operations_center.multi_agent_troubleshooter.src.agents.memory_agent import (
    MemoryAgent,
)
from operations_center.multi_agent_troubleshooter.src.models import AgentFinding


def test_memory_agent_name() -> None:
    """Verify that MemoryAgent exposes the expected agent name."""
    agent = MemoryAgent(llm_client=MagicMock())

    assert agent.name == "Memory Agent"


def test_memory_agent_investigate_returns_finding() -> None:
    """Verify that MemoryAgent converts the LLM response into AgentFinding."""

    mock_llm_client = MagicMock()
    mock_llm_client.generate.return_value = """
    {
        "agent_name": "Memory Agent",
        "summary": "Memory utilization increased significantly during the incident.",
        "evidence": [
            "Memory usage increased from 60% to 95%"
        ],
        "confidence": 0.92
    }
    """

    agent = MemoryAgent(llm_client=mock_llm_client)

    finding = agent.investigate(
        "Payment service returning HTTP 500 errors. "
        "Memory usage increased from 60% to 95%."
    )

    assert isinstance(finding, AgentFinding)
    assert finding.agent_name == "Memory Agent"
    assert finding.confidence == 0.92
    assert "Memory usage increased from 60% to 95%" in finding.evidence

    mock_llm_client.generate.assert_called_once()

def test_memory_agent_sends_memory_focused_prompt() -> None:
    """Verify that MemoryAgent sends a memory-focused prompt to the LLM."""

    mock_llm_client = MagicMock()
    mock_llm_client.generate.return_value = """
    {
        "agent_name": "Memory Agent",
        "summary": "No memory-related evidence was identified.",
        "evidence": [],
        "confidence": 0.95
    }
    """

    agent = MemoryAgent(llm_client=mock_llm_client)

    incident = "Payment service is returning HTTP 500 errors."
    agent.investigate(incident)

    prompt = mock_llm_client.generate.call_args.args[0]

    assert "Memory Agent" in prompt
    assert "Memory utilization" in prompt
    assert incident in prompt


def test_memory_agent_accepts_no_memory_evidence() -> None:
    """Verify that MemoryAgent can return a valid finding with no memory evidence."""

    mock_llm_client = MagicMock()
    mock_llm_client.generate.return_value = """
    {
        "agent_name": "Memory Agent",
        "summary": "No memory-related evidence was identified.",
        "evidence": [],
        "confidence": 0.95
    }
    """

    agent = MemoryAgent(llm_client=mock_llm_client)

    finding = agent.investigate(
        "Payment service is returning HTTP 500 errors."
    )

    assert isinstance(finding, AgentFinding)
    assert finding.evidence == []
    assert finding.summary == "No memory-related evidence was identified."


def test_memory_agent_raises_on_invalid_llm_response() -> None:
    """Verify that MemoryAgent rejects malformed LLM output."""

    mock_llm_client = MagicMock()
    mock_llm_client.generate.return_value = "not valid json"

    agent = MemoryAgent(llm_client=mock_llm_client)

    try:
        agent.investigate("Payment service is unavailable.")
        assert False, "Expected validation error"
    except ValueError:
        pass
