from unittest.mock import MagicMock

from operations_center.multi_agent_troubleshooter.src.coordinator.coordinator import (
    TroubleshootingCoordinator,
)
from operations_center.multi_agent_troubleshooter.src.models import (
    AgentFinding,
    TroubleshootingResult,
)


def test_coordinator_investigates_with_all_agents() -> None:
    """Verify that the coordinator runs every configured agent."""

    cpu_agent = MagicMock()
    cpu_agent.name = "CPU Agent"
    cpu_agent.investigate.return_value = AgentFinding(
        agent_name="CPU Agent",
        summary="High CPU detected.",
        evidence=["CPU usage reached 95%."],
        confidence=0.95,
    )

    memory_agent = MagicMock()
    memory_agent.name = "Memory Agent"
    memory_agent.investigate.return_value = AgentFinding(
        agent_name="Memory Agent",
        summary="High memory usage detected.",
        evidence=["Memory usage reached 95%."],
        confidence=0.90,
    )

    network_agent = MagicMock()
    network_agent.name = "Network Agent"
    network_agent.investigate.return_value = AgentFinding(
        agent_name="Network Agent",
        summary="Network latency increased.",
        evidence=["Latency increased to 2 seconds."],
        confidence=0.91,
    )

    coordinator = TroubleshootingCoordinator(
        agents=[cpu_agent, memory_agent, network_agent]
    )

    incident = "Payment service is returning HTTP 500 errors."

    result = coordinator.investigate(incident)

    assert isinstance(result, TroubleshootingResult)
    assert result.incident == incident
    assert len(result.findings) == 3

    assert result.findings[0].agent_name == "CPU Agent"
    assert result.findings[1].agent_name == "Memory Agent"
    assert result.findings[2].agent_name == "Network Agent"

    cpu_agent.investigate.assert_called_once_with(incident)
    memory_agent.investigate.assert_called_once_with(incident)
    network_agent.investigate.assert_called_once_with(incident)


def test_coordinator_with_no_agents_returns_empty_findings() -> None:
    """Verify that the coordinator handles an empty agent list."""

    coordinator = TroubleshootingCoordinator(agents=[])

    incident = "Payment service is unavailable."

    result = coordinator.investigate(incident)

    assert isinstance(result, TroubleshootingResult)
    assert result.incident == incident
    assert result.findings == []

def test_coordinator_continues_when_an_agent_fails() -> None:
    """Verify that one failing agent does not stop other agents."""

    cpu_agent = MagicMock()
    cpu_agent.name = "CPU Agent"
    cpu_agent.investigate.side_effect = RuntimeError("CPU agent failed")

    memory_agent = MagicMock()
    memory_agent.name = "Memory Agent"
    memory_agent.investigate.return_value = AgentFinding(
        agent_name="Memory Agent",
        summary="High memory usage detected.",
        evidence=["Memory usage reached 95%."],
        confidence=0.90,
    )

    network_agent = MagicMock()
    network_agent.name = "Network Agent"
    network_agent.investigate.return_value = AgentFinding(
        agent_name="Network Agent",
        summary="Network latency increased.",
        evidence=["Latency increased to 2 seconds."],
        confidence=0.91,
    )

    coordinator = TroubleshootingCoordinator(
        agents=[cpu_agent, memory_agent, network_agent]
    )

    incident = "Payment service is returning HTTP 500 errors."

    result = coordinator.investigate(incident)

    assert isinstance(result, TroubleshootingResult)
    assert result.incident == incident
    assert len(result.findings) == 2

    assert result.findings[0].agent_name == "Memory Agent"
    assert result.findings[1].agent_name == "Network Agent"

    cpu_agent.investigate.assert_called_once_with(incident)
    memory_agent.investigate.assert_called_once_with(incident)
    network_agent.investigate.assert_called_once_with(incident)