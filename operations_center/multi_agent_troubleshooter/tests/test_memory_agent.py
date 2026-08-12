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