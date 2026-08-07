from runbook_generator.src.prompts.runbook_prompt import RUNBOOK_PROMPT
from core.llm_client import LLMClient

class RunbookGenerator:

    def __init__(self):
        self.llm_client = LLMClient()

    def generate(self, incident: str) -> str:
        prompt = RUNBOOK_PROMPT.format(
            incident=incident
        )
        #TEST
        #prompt = RUNBOOK_PROMPT

        return self.llm_client.generate(prompt)