"""Prompt construction for the Postmortem Generator capability."""

from incident_management.postmortem_generator.src.models import Postmortem


def build_postmortem_prompt(incident_evidence: str) -> str:
    """Build the prompt used to generate a structured incident postmortem."""

    schema = Postmortem.model_json_schema()

    return f"""
You are an experienced Site Reliability Engineer creating a blameless incident postmortem.

Use only the incident evidence provided below.

Rules:
- Do not invent facts.
- Clearly distinguish confirmed root causes from hypotheses.
- If evidence is insufficient, use root_cause.status = "unknown" or "hypothesis".
- Timeline events must be supported by the supplied evidence.
- Corrective actions should address immediate weaknesses exposed by the incident.
- Preventive actions should reduce the likelihood or impact of recurrence.
- Keep the postmortem factual, concise, and blameless.
- Return valid JSON only.
- Do not include Markdown code fences or additional commentary.

Required JSON schema:
{schema}

Incident evidence:
{incident_evidence}
""".strip()
