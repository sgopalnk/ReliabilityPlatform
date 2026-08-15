"""Tests for Postmortem Generator Pydantic models."""

import pytest
from pydantic import ValidationError

from incident_management.postmortem_generator.src.models import (
    ActionItem,
    Postmortem,
    RootCause,
    TimelineEvent,
)


def test_postmortem_model_accepts_valid_data() -> None:
    """Verify that a valid structured postmortem can be created."""

    postmortem = Postmortem(
        incident_summary="Payment API returned elevated 500 errors.",
        impact="Customers were unable to complete payments for 20 minutes.",
        timeline=[
            TimelineEvent(
                timestamp="2026-08-15T10:00:00Z",
                event="Error rate exceeded alert threshold.",
                evidence=["Monitoring alert triggered."],
            )
        ],
        root_cause=RootCause(
            statement="Database connection pool exhaustion caused request failures.",
            status="hypothesis",
            evidence=["Connection timeout errors increased during the incident."],
        ),
        contributing_factors=["Insufficient connection pool capacity."],
        what_went_well=["Alerting detected the issue quickly."],
        what_went_poorly=["Diagnosis required manual log correlation."],
        corrective_actions=[
            ActionItem(
                action="Increase connection pool capacity.",
                rationale="Reduce immediate risk of exhaustion.",
            )
        ],
        preventive_actions=[
            ActionItem(
                action="Add connection pool saturation alerts.",
                rationale="Detect capacity pressure before failures occur.",
            )
        ],
        lessons_learned=[
            "Connection pool saturation should be monitored as a leading indicator."
        ],
    )

    assert postmortem.root_cause.status == "hypothesis"
    assert len(postmortem.timeline) == 1
    assert len(postmortem.corrective_actions) == 1


def test_root_cause_rejects_invalid_status() -> None:
    """Verify that unsupported root-cause statuses are rejected."""

    with pytest.raises(ValidationError):
        RootCause(
            statement="Unknown failure.",
            status="probable",
            evidence=[],
        )
