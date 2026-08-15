from unittest.mock import MagicMock

from operations_center.multi_agent_troubleshooter.src.agents.network_agent import (
    NetworkAgent,
)
from operations_center.multi_agent_troubleshooter.src.models import AgentFinding


def test_network_agent_name() -> None:
    """Verify that NetworkAgent exposes the expected agent name."""
    agent = NetworkAgent(llm_client=MagicMock())

    assert agent.name == "Network Agent"


def test_network_agent_investigate_returns_finding() -> None:
    """Verify that NetworkAgent converts the LLM response into AgentFinding."""

    mock_llm_client = MagicMock()
    mock_llm_client.generate.return_value = """
    {
        "agent_name": "Network Agent",
        "summary": "Network latency increased significantly during the incident.",
        "evidence": [
            "Request latency increased from 100ms to 2 seconds"
        ],
        "confidence": 0.91
    }
    """

    agent = NetworkAgent(llm_client=mock_llm_client)

    finding = agent.investigate(
        "Payment service returning HTTP 500 errors. "
        "Request latency increased from 100ms to 2 seconds."
    )

    assert isinstance(finding, AgentFinding)
    assert finding.agent_name == "Network Agent"
    assert finding.confidence == 0.91
    assert "Request latency increased from 100ms to 2 seconds" in finding.evidence

    mock_llm_client.generate.assert_called_once()

def test_network_agent_sends_network_focused_prompt() -> None:
    """Verify that NetworkAgent sends a network-focused prompt to the LLM."""

    mock_llm_client = MagicMock()
    mock_llm_client.generate.return_value = """
    {
        "agent_name": "Network Agent",
        "summary": "No network-related evidence was identified.",
        "evidence": [],
        "confidence": 0.95
    }
    """

    agent = NetworkAgent(llm_client=mock_llm_client)

    incident = "Payment service is returning HTTP 500 errors."
    agent.investigate(incident)

    prompt = mock_llm_client.generate.call_args.args[0]

    assert "Network Agent" in prompt
    assert "Network connectivity" in prompt
    assert incident in prompt


def test_network_agent_accepts_no_network_evidence() -> None:
    """Verify that NetworkAgent can return a valid finding with no network evidence."""

    mock_llm_client = MagicMock()
    mock_llm_client.generate.return_value = """
    {
        "agent_name": "Network Agent",
        "summary": "No network-related evidence was identified.",
        "evidence": [],
        "confidence": 0.95
    }
    """

    agent = NetworkAgent(llm_client=mock_llm_client)

    finding = agent.investigate(
        "Payment service is returning HTTP 500 errors."
    )

    assert isinstance(finding, AgentFinding)
    assert finding.evidence == []
    assert finding.summary == "No network-related evidence was identified."


def test_network_agent_raises_on_invalid_llm_response() -> None:
    """Verify that NetworkAgent rejects malformed LLM output."""

    mock_llm_client = MagicMock()
    mock_llm_client.generate.return_value = "not valid json"

    agent = NetworkAgent(llm_client=mock_llm_client)

    try:
        agent.investigate("Payment service is unavailable.")
        assert False, "Expected validation error"
    except ValueError:
        pass
