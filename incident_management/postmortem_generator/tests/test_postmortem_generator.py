"""Tests for the Postmortem Generator service."""

import json
from unittest.mock import MagicMock

import pytest

from incident_management.postmortem_generator.src.services.postmortem_generator import (
    PostmortemGenerator,
)


def valid_postmortem_response() -> str:
    """Return a valid serialized Postmortem response."""

    return json.dumps(
        {
            "incident_summary": "Payment API experienced elevated HTTP 500 errors.",
            "impact": "Customers could not complete payments for 20 minutes.",
            "timeline": [
                {
                    "timestamp": "2026-08-15T10:00:00Z",
                    "event": "Error rate exceeded alert threshold.",
                    "evidence": ["Monitoring alert triggered."],
                }
            ],
            "root_cause": {
                "statement": "Database connection pool exhaustion caused failures.",
                "status": "hypothesis",
                "evidence": [
                    "Connection timeout errors increased during the incident."
                ],
            },
            "contributing_factors": [
                "Insufficient connection pool capacity."
            ],
            "what_went_well": [
                "Alerting detected the issue quickly."
            ],
            "what_went_poorly": [
                "Diagnosis required manual log correlation."
            ],
            "corrective_actions": [
                {
                    "action": "Increase connection pool capacity.",
                    "rationale": "Reduce immediate risk of exhaustion.",
                }
            ],
            "preventive_actions": [
                {
                    "action": "Add connection pool saturation alerts.",
                    "rationale": "Detect capacity pressure before failures occur.",
                }
            ],
            "lessons_learned": [
                "Connection pool saturation should be monitored proactively."
            ],
        }
    )


def test_generate_returns_valid_postmortem() -> None:
    """Verify that valid LLM output is converted into a Postmortem."""

    llm_client = MagicMock()
    llm_client.generate.return_value = valid_postmortem_response()

    generator = PostmortemGenerator(llm_client=llm_client)

    result = generator.generate(
        "Payment API returned elevated HTTP 500 errors."
    )

    assert result.incident_summary.startswith("Payment API")
    assert result.root_cause.status == "hypothesis"
    assert len(result.corrective_actions) == 1

    llm_client.generate.assert_called_once()


def test_generate_rejects_invalid_json() -> None:
    """Verify that invalid JSON from the LLM is rejected."""

    llm_client = MagicMock()
    llm_client.generate.return_value = "not valid json"

    generator = PostmortemGenerator(llm_client=llm_client)

    with pytest.raises(ValueError, match="invalid JSON"):
        generator.generate("Example incident evidence.")


def test_generate_rejects_invalid_schema() -> None:
    """Verify that incomplete structured output is rejected."""

    llm_client = MagicMock()
    llm_client.generate.return_value = json.dumps(
        {
            "incident_summary": "Example incident."
        }
    )

    generator = PostmortemGenerator(llm_client=llm_client)

    with pytest.raises(ValueError, match="Postmortem schema"):
        generator.generate("Example incident evidence.")
