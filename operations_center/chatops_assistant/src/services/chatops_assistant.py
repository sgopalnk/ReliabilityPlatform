"""
ChatOps Assistant

Answers Reliability Engineering questions using the configured
Large Language Model (LLM) and converts the response
into a structured ChatResponse object.
"""

import json
from json import JSONDecodeError

import openai
from pydantic import ValidationError

from core.llm_client import LLMClient
from core.logger import get_logger

from operations_center.chatops_assistant.src.exceptions import ChatOpsAssistantError
from operations_center.chatops_assistant.src.models import ChatResponse
from operations_center.chatops_assistant.src.prompt_builder import PromptBuilder

logger = get_logger("chatops_assistant")


class ChatOpsAssistant:
    """
    Answers Reliability Engineering questions using an LLM.
    """

    def __init__(self):
        # Create a reusable LLM client.
        self.llm_client = LLMClient()

    def answer(self, question: str) -> ChatResponse:
        """
        Answer a Reliability Engineering question and return
        a structured ChatResponse object.
        """
        logger.info("Starting ChatOps request.")

        # 1. Build the prompt.
        prompt = PromptBuilder.build(question)

        try:
            logger.info("Sending question to LLM.")

            # 2. Send the prompt to the configured LLM.
            response_text = self.llm_client.generate(prompt)

            # 3. Convert JSON text to Python dictionary.
            response_json = json.loads(response_text)

            # 4. Convert dictionary to ChatResponse object.
            response = ChatResponse(**response_json)

            logger.info("ChatOps request completed successfully.")

            # 5. Return the object.
            return response

        except openai.APIError as e:
            logger.exception("Failed to communicate with LLM provider.")
            raise ChatOpsAssistantError(
                "Unable to connect to the LLM provider."
            ) from e

        except JSONDecodeError as e:
            logger.exception("LLM returned invalid JSON.")
            raise ChatOpsAssistantError(
                "The AI returned invalid JSON."
            ) from e

        except ValidationError as e:
            logger.exception("LLM response failed schema validation.")
            raise ChatOpsAssistantError(
                "The AI response did not match the expected schema."
            ) from e