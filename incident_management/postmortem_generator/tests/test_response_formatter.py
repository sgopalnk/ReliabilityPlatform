"""Tests for Postmortem Generator response formatting."""

from incident_management.postmortem_generator.src.models import (
    ActionItem,
    Postmortem,
    RootCause,
    TimelineEvent,
)
from incident_management.postmortem_generator.src.response_formatter import (
    format_postmortem,
)


def test_format_postmortem_contains_required_sections() -> None:
    """Verify that formatted output contains all major postmortem sections."""

    postmortem = Postmortem(
        incident_summary="Payment API experienced failures.",
        impact="Payment attempts failed for some customers.",
        timeline=[
            TimelineEvent(
                timestamp="10:00 UTC",
                event="Alert triggered.",
                evidence=["HTTP 500 rate exceeded threshold."],
            )
        ],
        root_cause=RootCause(
            statement="Connection pool exhaustion suspected.",
            status="hypothesis",
            evidence=["Database timeout errors observed."],
        ),
        contributing_factors=["Capacity margin was insufficient."],
        what_went_well=["Alerting detected the incident."],
        what_went_poorly=["Diagnosis was manual."],
        corrective_actions=[
            ActionItem(
                action="Increase connection pool capacity.",
                rationale="Restore adequate capacity margin.",
            )
        ],
        preventive_actions=[
            ActionItem(
                action="Monitor pool saturation.",
                rationale="Detect exhaustion risk earlier.",
            )
        ],
        lessons_learned=["Pool saturation is a useful leading indicator."],
    )

    result = format_postmortem(postmortem)

    assert "# Incident Postmortem" in result
    assert "## Impact" in result
    assert "## Timeline" in result
    assert "## Root Cause" in result
    assert "**Status:** hypothesis" in result
    assert "## Contributing Factors" in result
    assert "## What Went Well" in result
    assert "## What Went Poorly" in result
    assert "## Corrective Actions" in result
    assert "## Preventive Actions" in result
    assert "## Lessons Learned" in result
