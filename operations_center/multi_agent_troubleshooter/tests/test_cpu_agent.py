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
