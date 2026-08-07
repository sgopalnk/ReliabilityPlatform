def build_incident_prompt(incident: str) -> str:
    """
    Build the prompt for incident analysis.
    Prompt should define - AI role, the task, the desired reasoning.
    """

    return f"""
You are a Senior Site Reliability Engineer (SRE).

Analyze the production incident below.

Analyze the incident in normal English.

The JSON must contain exactly these fields:

- executive_summary (string)
- possible_root_cause (string)
- confidence_level (string)
- immediate_actions (array of strings)
- business_impact (string)

Do not include markdown.
Do not include explanations.
Do not wrap the JSON in ```.

Incident:

{incident}
    """.strip()