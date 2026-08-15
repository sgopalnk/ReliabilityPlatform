import logging

from core.llm_client import LLMClient
from core.logger import get_logger

from operations_center.multi_agent_troubleshooter.src.models import (
    SynthesisResult,
    TroubleshootingResult,
)
from operations_center.multi_agent_troubleshooter.src.prompts.synthesis_prompt import (
    SYNTHESIS_SYSTEM_PROMPT,
)

logger: logging.Logger = get_logger(
    "multi_agent_troubleshooter.synthesizer"
)


class FindingSynthesizer:
    """Synthesize findings from multiple troubleshooting agents."""

    def __init__(self, llm_client: LLMClient | None = None) -> None:
        self._llm_client = llm_client or LLMClient()

    def synthesize(
        self,
        troubleshooting_result: TroubleshootingResult,
    ) -> SynthesisResult:
        """Produce an evidence-based synthesis of agent findings."""

        logger.info(
            "Starting finding synthesis. Status=%s, findings=%d, failures=%d.",
            troubleshooting_result.status,
            len(troubleshooting_result.findings),
            len(troubleshooting_result.failures),
        )

        prompt = f"""
{SYNTHESIS_SYSTEM_PROMPT}

Incident:

{troubleshooting_result.incident}

Investigation status:

{troubleshooting_result.status}

Agent findings:

{troubleshooting_result.findings}

Agent failures:

{troubleshooting_result.failures}

Return a JSON object with exactly these fields:

- summary: string
- key_findings: array of strings
- correlations: array of strings
- conflicts: array of strings
- root_cause_hypothesis: string
- confidence: number between 0.0 and 1.0

Return only valid JSON. Do not include markdown or additional text.
"""

        response = self._llm_client.generate(prompt)

        result = SynthesisResult.model_validate_json(response)

        logger.info(
            "Finding synthesis completed successfully. Confidence=%.2f.",
            result.confidence,
        )

        return result
