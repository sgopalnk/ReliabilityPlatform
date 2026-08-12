from core.llm_client import LLMClient

from operations_center.multi_agent_troubleshooter.src.agents.base_agent import BaseAgent
from operations_center.multi_agent_troubleshooter.src.models import AgentFinding
from operations_center.multi_agent_troubleshooter.src.prompts.memory_agent_prompt import (
    MEMORY_AGENT_SYSTEM_PROMPT,
)


class MemoryAgent(BaseAgent):
    """Troubleshooting agent focused on memory-related incident evidence."""

    def __init__(self, llm_client: LLMClient | None = None) -> None:
        self._llm_client = llm_client or LLMClient()

    @property
    def name(self) -> str:
        """Return the unique name of this agent."""
        return "Memory Agent"

    def investigate(self, incident: str) -> AgentFinding:
        """Investigate memory-related evidence in an incident."""

        prompt = f"""
{MEMORY_AGENT_SYSTEM_PROMPT}

Analyze the following incident:

{incident}

Return a JSON object with exactly these fields:
- agent_name: string
- summary: string
- evidence: array of strings
- confidence: number between 0.0 and 1.0

Return only valid JSON. Do not include markdown or additional text.
"""

        response = self._llm_client.generate(prompt)

        return AgentFinding.model_validate_json(response)