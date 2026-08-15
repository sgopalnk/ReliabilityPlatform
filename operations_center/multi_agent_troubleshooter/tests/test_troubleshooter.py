from unittest.mock import MagicMock, patch

from operations_center.multi_agent_troubleshooter.src.models import (
    AgentFinding,
    TroubleshootingAnalysis,
    TroubleshootingResult,
)
from operations_center.multi_agent_troubleshooter.src.services.troubleshooter import (
    MultiAgentTroubleshooter,
)
from operations_center.multi_agent_troubleshooter.src.agents.cpu_agent import CPUAgent
from operations_center.multi_agent_troubleshooter.src.agents.memory_agent import MemoryAgent
from operations_center.multi_agent_troubleshooter.src.agents.network_agent import NetworkAgent


def test_troubleshooter_investigate() -> None:
    """Verify that the service delegates investigation to the coordinator."""

    expected_result = TroubleshootingResult(
        incident="Payment service is unavailable.",
        findings=[
            AgentFinding(
                agent_name="CPU Agent",
                summary="High CPU detected.",
                evidence=["CPU usage reached 95%."],
                confidence=0.95,
            )
        ],
        status="completed",
    )

    with patch(
        "operations_center.multi_agent_troubleshooter.src.services.troubleshooter."
        "TroubleshootingCoordinator"
    ) as coordinator_class:
        coordinator = MagicMock()
        coordinator.investigate.return_value = expected_result
        coordinator_class.return_value = coordinator

        troubleshooter = MultiAgentTroubleshooter()

        result = troubleshooter.investigate(
            "Payment service is unavailable."
        )

    assert isinstance(result, TroubleshootingAnalysis)
    assert result.investigation == expected_result

    coordinator.investigate.assert_called_once_with(
        "Payment service is unavailable."
    )

def test_troubleshooter_accepts_custom_agents() -> None:
    """Verify that the service accepts a custom agent list."""
    custom_agent = MagicMock()

    troubleshooter = MultiAgentTroubleshooter(
        agents=[custom_agent]
    )

    assert troubleshooter._coordinator._agents == [custom_agent]

def test_troubleshooter_uses_injected_agents() -> None:
    """Verify that the service uses explicitly provided agents."""

    cpu_agent = MagicMock()
    memory_agent = MagicMock()

    expected_result = TroubleshootingResult(
        incident="Payment service is unavailable.",
        findings=[],
        status="failed",
    )

    coordinator = MagicMock()
    coordinator.investigate.return_value = expected_result

    with patch(
        "operations_center.multi_agent_troubleshooter.src.services.troubleshooter."
        "TroubleshootingCoordinator"
    ) as coordinator_class:
        coordinator_class.return_value = coordinator

        troubleshooter = MultiAgentTroubleshooter(
            agents=[cpu_agent, memory_agent]
        )

    coordinator_class.assert_called_once_with(
        agents=[cpu_agent, memory_agent]
    )

def test_troubleshooter_creates_default_agents() -> None:
    """Verify that the service creates the default troubleshooting agents."""

    with patch(
        "operations_center.multi_agent_troubleshooter.src.services.troubleshooter."
        "TroubleshootingCoordinator"
    ) as coordinator_class:
        coordinator = MagicMock()
        coordinator_class.return_value = coordinator

        MultiAgentTroubleshooter()

    agents = coordinator_class.call_args.kwargs["agents"]

    assert len(agents) == 3
    assert isinstance(agents[0], CPUAgent)
    assert isinstance(agents[1], MemoryAgent)
    assert isinstance(agents[2], NetworkAgent)


def test_troubleshooter_rejects_empty_incident() -> None:
    """Verify that an empty incident is rejected."""
    troubleshooter = MultiAgentTroubleshooter()

    try:
        troubleshooter.investigate("")
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert str(exc) == "Incident description cannot be empty."


def test_troubleshooter_rejects_whitespace_only_incident() -> None:
    """Verify that a whitespace-only incident is rejected."""
    troubleshooter = MultiAgentTroubleshooter()

    try:
        troubleshooter.investigate("   ")
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert str(exc) == "Incident description cannot be empty."


def test_troubleshooter_propagates_synthesis_failure() -> None:
    """Verify that a synthesis failure is propagated to the caller."""

    synthesizer = MagicMock()
    synthesizer.synthesize.side_effect = RuntimeError("Synthesis failed")

    troubleshooter = MultiAgentTroubleshooter(
        agents=[],
        synthesizer=synthesizer,
    )

    try:
        troubleshooter.investigate("Payment service is unavailable.")
        assert False, "Expected RuntimeError"
    except RuntimeError as exc:
        assert str(exc) == "Synthesis failed"

    synthesizer.synthesize.assert_called_once()
