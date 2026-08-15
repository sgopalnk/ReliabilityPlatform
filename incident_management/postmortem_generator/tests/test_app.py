"""Tests for the Postmortem Generator CLI."""

import sys
from unittest.mock import MagicMock, patch

import pytest

from incident_management.postmortem_generator import app
from incident_management.postmortem_generator.src.models import (
    ActionItem,
    Postmortem,
    RootCause,
    TimelineEvent,
)


def sample_postmortem() -> Postmortem:
    """Return a valid Postmortem for CLI testing."""

    return Postmortem(
        incident_summary="Payment service experienced failures.",
        impact="Some payment attempts failed.",
        timeline=[
            TimelineEvent(
                timestamp="10:02 UTC",
                event="Alert triggered.",
                evidence=["HTTP 500 rate increased."],
            )
        ],
        root_cause=RootCause(
            statement="Connection pool exhaustion is suspected.",
            status="hypothesis",
            evidence=["Database connection timeouts observed."],
        ),
        contributing_factors=["Connection pool utilization was high."],
        what_went_well=["Monitoring detected the incident quickly."],
        what_went_poorly=["Diagnosis required manual correlation."],
        corrective_actions=[
            ActionItem(
                action="Review connection pool capacity.",
                rationale="Reduce immediate saturation risk.",
            )
        ],
        preventive_actions=[
            ActionItem(
                action="Add connection pool saturation alerts.",
                rationale="Detect capacity pressure earlier.",
            )
        ],
        lessons_learned=["Pool saturation should be monitored proactively."],
    )


def test_main_generates_formatted_postmortem(tmp_path, capsys) -> None:
    """Verify that the CLI reads evidence and prints a postmortem."""

    incident_file = tmp_path / "incident.txt"
    incident_file.write_text("Example incident evidence.", encoding="utf-8")

    mock_generator = MagicMock()
    mock_generator.generate.return_value = sample_postmortem()

    with (
        patch.object(sys, "argv", ["app", str(incident_file)]),
        patch.object(app, "PostmortemGenerator", return_value=mock_generator),
    ):
        app.main()

    output = capsys.readouterr().out

    assert "# Incident Postmortem" in output
    assert "## Root Cause" in output
    assert "**Status:** hypothesis" in output

    mock_generator.generate.assert_called_once_with(
        "Example incident evidence."
    )


def test_main_rejects_missing_argument() -> None:
    """Verify that the CLI requires an incident evidence file."""

    with patch.object(sys, "argv", ["app"]):
        with pytest.raises(SystemExit):
            app.main()
