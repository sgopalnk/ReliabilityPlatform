from unittest.mock import MagicMock, patch

from operations_center.multi_agent_troubleshooter.src.models import (
    AgentFinding,
    TroubleshootingResult,
)
from operations_center.multi_agent_troubleshooter.src.services.troubleshooter import (
    MultiAgentTroubleshooter,
)


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

    assert isinstance(result, TroubleshootingResult)
    assert result == expected_result

    coordinator.investigate.assert_called_once_with(
        "Payment service is unavailable."
    )