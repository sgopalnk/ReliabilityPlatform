from unittest.mock import MagicMock

from operations_center.multi_agent_troubleshooter.src.agents.cpu_agent import CPUAgent
from operations_center.multi_agent_troubleshooter.src.agents.memory_agent import MemoryAgent
from operations_center.multi_agent_troubleshooter.src.agents.network_agent import NetworkAgent
from operations_center.multi_agent_troubleshooter.src.coordinator.coordinator import (
    TroubleshootingCoordinator,
)
from operations_center.multi_agent_troubleshooter.src.models import (
    TroubleshootingResult,
)


def test_troubleshooting_coordinator_with_real_agents() -> None:
    """Verify that the coordinator orchestrates the real troubleshooting agents."""

    cpu_llm = MagicMock()
    cpu_llm.generate.return_value = """
    {
        "agent_name": "CPU Agent",
        "summary": "High CPU utilization detected.",
        "evidence": ["CPU usage reached 95%."],
        "confidence": 0.95
    }
    """

    memory_llm = MagicMock()
    memory_llm.generate.return_value = """
    {
        "agent_name": "Memory Agent",
        "summary": "High memory utilization detected.",
        "evidence": ["Memory usage reached 95%."],
        "confidence": 0.90
    }
    """

    network_llm = MagicMock()
    network_llm.generate.return_value = """
    {
        "agent_name": "Network Agent",
        "summary": "Network latency increased.",
        "evidence": ["Latency increased to 2 seconds."],
        "confidence": 0.91
    }
    """

    cpu_agent = CPUAgent(llm_client=cpu_llm)
    memory_agent = MemoryAgent(llm_client=memory_llm)
    network_agent = NetworkAgent(llm_client=network_llm)

    coordinator = TroubleshootingCoordinator(
        agents=[cpu_agent, memory_agent, network_agent]
    )

    incident = (
        "Payment service is returning HTTP 500 errors. "
        "CPU usage increased to 95%. "
        "Memory usage increased to 95%. "
        "Network latency increased to 2 seconds."
    )

    result = coordinator.investigate(incident)

    assert isinstance(result, TroubleshootingResult)
    assert result.incident == incident
    assert len(result.findings) == 3

    assert result.findings[0].agent_name == "CPU Agent"
    assert result.findings[1].agent_name == "Memory Agent"
    assert result.findings[2].agent_name == "Network Agent"

    cpu_llm.generate.assert_called_once()
    memory_llm.generate.assert_called_once()
    network_llm.generate.assert_called_once()