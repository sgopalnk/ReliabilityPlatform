"""Tests for the Postmortem Generator prompt builder."""

from incident_management.postmortem_generator.src.prompt_builder import (
    build_postmortem_prompt,
)


def test_prompt_contains_incident_evidence() -> None:
    """Verify that supplied incident evidence is included in the prompt."""

    incident_evidence = "Payment API experienced elevated HTTP 500 errors."

    prompt = build_postmortem_prompt(incident_evidence)

    assert incident_evidence in prompt


def test_prompt_requires_evidence_based_output() -> None:
    """Verify that the prompt prevents unsupported conclusions."""

    prompt = build_postmortem_prompt("Database timeout observed.")

    assert "Do not invent facts." in prompt
    assert "confirmed root causes from hypotheses" in prompt
    assert "Return valid JSON only." in prompt


def test_prompt_contains_postmortem_schema() -> None:
    """Verify that the structured Postmortem schema is included."""

    prompt = build_postmortem_prompt("Example incident.")

    assert "incident_summary" in prompt
    assert "root_cause" in prompt
    assert "corrective_actions" in prompt
    assert "preventive_actions" in prompt
    assert "lessons_learned" in prompt
