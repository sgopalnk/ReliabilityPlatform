# Postmortem Generator

The Postmortem Generator creates structured, evidence-based incident postmortems from incident evidence.

## MVP Capabilities

The generated postmortem includes:

- Incident summary
- Impact
- Timeline
- Root cause or root-cause hypothesis
- Contributing factors
- What went well
- What went poorly
- Corrective actions
- Preventive actions
- Lessons learned

The generator explicitly distinguishes confirmed root causes from hypotheses and unknown causes.

## Architecture

The capability uses the shared ReliabilityPlatform components:

- `core.llm_client.LLMClient` for provider-agnostic LLM access
- `core.logger` for logging
- Pydantic models for structured output validation

Flow:

Incident Evidence -> Prompt Builder -> LLMClient -> Pydantic Validation -> Postmortem -> Formatter

The Postmortem Generator does not directly depend on Incident Commander or Multi-Agent Troubleshooter. This keeps the capability independently usable while allowing their structured outputs to be integrated later.

## Usage

From the ReliabilityPlatform repository root:

    python -m incident_management.postmortem_generator.app <incident_file>

Example:

    python -m incident_management.postmortem_generator.app \
      incident_management/postmortem_generator/sample_data/payment-service-incident.txt

## Tests

Run module tests:

    pytest incident_management/postmortem_generator/tests -v

Run the complete ReliabilityPlatform test suite:

    pytest
