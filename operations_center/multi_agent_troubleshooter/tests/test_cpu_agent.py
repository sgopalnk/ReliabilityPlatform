from unittest.mock import MagicMock

from operations_center.multi_agent_troubleshooter.src.agents.cpu_agent import CPUAgent
from operations_center.multi_agent_troubleshooter.src.models import AgentFinding


def test_cpu_agent_name() -> None:
    """Verify that CPUAgent exposes the expected agent name."""
    agent = CPUAgent(llm_client=MagicMock())

    assert agent.name == "CPU Agent"


def test_cpu_agent_investigate_returns_finding() -> None:
    """Verify that CPUAgent converts the LLM response into AgentFinding."""

    mock_llm_client = MagicMock()
    mock_llm_client.generate.return_value = """
    {
        "agent_name": "CPU Agent",
        "summary": "CPU utilization increased significantly during the incident.",
        "evidence": [
            "CPU usage increased from 35% to 95%"
        ],
        "confidence": 0.95
    }
    """

    agent = CPUAgent(llm_client=mock_llm_client)

    finding = agent.investigate(
        "Payment service returning HTTP 500 errors. "
        "CPU usage increased from 35% to 95%."
    )

    assert isinstance(finding, AgentFinding)
    assert finding.agent_name == "CPU Agent"
    assert finding.confidence == 0.95
    assert "CPU usage increased from 35% to 95%" in finding.evidence

    mock_llm_client.generate.assert_called_once()

def test_cpu_agent_sends_cpu_focused_prompt() -> None:
    """Verify that CPUAgent sends a CPU-focused prompt to the LLM."""

    mock_llm_client = MagicMock()
    mock_llm_client.generate.return_value = """
    {
        "agent_name": "CPU Agent",
        "summary": "No CPU-related evidence was identified.",
        "evidence": [],
        "confidence": 0.95
    }
    """

    agent = CPUAgent(llm_client=mock_llm_client)

    incident = "Payment service is returning HTTP 500 errors."
    agent.investigate(incident)

    prompt = mock_llm_client.generate.call_args.args[0]

    assert "CPU Agent" in prompt
    assert "CPU utilization" in prompt
    assert incident in prompt


def test_cpu_agent_accepts_no_cpu_evidence() -> None:
    """Verify that CPUAgent can return a valid finding with no CPU evidence."""

    mock_llm_client = MagicMock()
    mock_llm_client.generate.return_value = """
    {
        "agent_name": "CPU Agent",
        "summary": "No CPU-related evidence was identified.",
        "evidence": [],
        "confidence": 0.95
    }
    """

    agent = CPUAgent(llm_client=mock_llm_client)

    finding = agent.investigate(
        "Payment service is returning HTTP 500 errors."
    )

    assert isinstance(finding, AgentFinding)
    assert finding.evidence == []
    assert finding.summary == "No CPU-related evidence was identified."


def test_cpu_agent_raises_on_invalid_llm_response() -> None:
    """Verify that CPUAgent rejects malformed LLM output."""

    mock_llm_client = MagicMock()
    mock_llm_client.generate.return_value = "not valid json"

    agent = CPUAgent(llm_client=mock_llm_client)

    try:
        agent.investigate("Payment service is unavailable.")
        assert False, "Expected validation error"
    except ValueError:
        pass
