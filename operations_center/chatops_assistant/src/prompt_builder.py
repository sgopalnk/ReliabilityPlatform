"""
Builds prompts for the ChatOps Assistant.
"""

from operations_center.chatops_assistant.src.prompts.system_prompt import (
    SYSTEM_PROMPT,
)


class PromptBuilder:
    """
    Builds the complete prompt sent to the LLM.
    """

    @staticmethod
    def build(question: str) -> str:
        """
        Build the prompt for the user's question.

        Args:
            question: User's natural language question.

        Returns:
            Complete prompt to send to the LLM.
        """

        return f"""{SYSTEM_PROMPT}

User Question:
{question}

Return ONLY valid JSON.

The JSON must exactly match this schema:

{{
    "answer": "string"
}}

Rules:

- Return only a single valid JSON object.
- Do not return any additional fields.
- Do not include explanations outside the JSON.
- The "answer" field should contain the complete response.
"""