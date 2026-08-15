"""Service for generating structured incident postmortems."""

import json

from pydantic import ValidationError

from core.llm_client import LLMClient
from core.logger import get_logger
from incident_management.postmortem_generator.src.models import Postmortem
from incident_management.postmortem_generator.src.prompt_builder import (
    build_postmortem_prompt,
)

logger = get_logger("postmortem_generator")


class PostmortemGenerator:
    """Generate structured postmortems from incident evidence."""

    def __init__(self, llm_client: LLMClient | None = None) -> None:
        """Initialize the generator with an optional LLM client."""

        self.llm_client = llm_client or LLMClient()

    def generate(self, incident_evidence: str) -> Postmortem:
        """Generate and validate a structured postmortem."""

        logger.info("Generating incident postmortem")

        prompt = build_postmortem_prompt(incident_evidence)
        response = self.llm_client.generate(prompt)

        try:
            data = json.loads(response)
            postmortem = Postmortem.model_validate(data)
        except json.JSONDecodeError as exc:
            logger.error("LLM returned invalid JSON")
            raise ValueError("LLM returned invalid JSON") from exc
        except ValidationError as exc:
            logger.error("LLM response did not match Postmortem schema")
            raise ValueError("LLM response did not match Postmortem schema") from exc

        logger.info("Incident postmortem generated successfully")

        return postmortem
