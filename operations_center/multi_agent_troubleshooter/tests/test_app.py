import json
from unittest.mock import MagicMock, patch

from operations_center.multi_agent_troubleshooter import app
from operations_center.multi_agent_troubleshooter.src.models import (
    AgentFinding,
    TroubleshootingResult,
)


def test_main_runs_troubleshooter_and_prints_result(capsys) -> None:
    """Verify that app.py invokes the troubleshooter and prints JSON."""

    result = TroubleshootingResult(
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
        "operations_center.multi_agent_troubleshooter.app.MultiAgentTroubleshooter"
    ) as troubleshooter_class:
        troubleshooter = MagicMock()
        troubleshooter.investigate.return_value = result
        troubleshooter_class.return_value = troubleshooter

        with patch(
            "sys.argv",
            [
                "app.py",
                "Payment service is unavailable.",
            ],
        ):
            app.main()

    output = capsys.readouterr().out
    parsed = json.loads(output)

    assert parsed["incident"] == "Payment service is unavailable."
    assert len(parsed["findings"]) == 1
    assert parsed["findings"][0]["agent_name"] == "CPU Agent"

    troubleshooter.investigate.assert_called_once_with(
        "Payment service is unavailable."
    )


def test_main_without_incident_prints_usage(capsys) -> None:
    """Verify that app.py shows usage when no incident is provided."""

    with patch("sys.argv", ["app.py"]):
        app.main()

    output = capsys.readouterr().out

    assert "Usage:" in output