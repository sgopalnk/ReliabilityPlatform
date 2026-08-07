"""
Currently implemented using the OpenAI SDK.
Future versions may support Anthropic, Gemini, Ollama,
or other providers without changing the rest of the application.
"""

from openai import OpenAI
from core.config import LLM_API_KEY, LLM_MODEL

class LLMClient:
    """
    Wrapper around the configured LLM provider.
    """

    def __init__(self):
        # Internal OpenAI client. The rest of the application
        # interacts only with LLMClient, not the OpenAI SDK.
        self._client = OpenAI(api_key=LLM_API_KEY)

    def generate(self, prompt: str) -> str:
        """
        Send a prompt to the configured LLM and return the generated response.
        """

        response = self._client.responses.create(
            model=LLM_MODEL,
            input=prompt
        )

        return response.output_text