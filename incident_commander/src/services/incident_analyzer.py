"""
Incident Analyzer

Analyzes production incidents using the configured
Large Language Model (LLM) and converts the response
into a structured IncidentAnalysis object.
"""
import json
import openai

from core.llm_client import LLMClient
from incident_commander.src.prompts.incident_prompt import build_incident_prompt
from incident_commander.src.models.incident_analysis import IncidentAnalysis
from incident_commander.src.exceptions import IncidentAnalysisError
from json import JSONDecodeError
from pydantic import ValidationError


class IncidentAnalyzer:
    """
    Analyzes production incidents using an LLM.
    """

    def __init__(self):
        # Create a reusable LLM client.
        self.llm_client = LLMClient()

    def analyze(self, incident: str) -> IncidentAnalysis:
        """
        Analyze a production incident and return a structured
        IncidentAnalysis object.
        """

        # 1. Build the prompt
        prompt = build_incident_prompt(incident)

        try:
            # 2. Send the prompt to the configured LLM.
            response_text = self.llm_client.generate(prompt)

            # 3. Convert JSON text to Python dictionary
            response_json = json.loads(response_text)
            # TEST - JSONDecodeError
            # response_json = json.loads("Hello")

            # 4. Convert dictionary to IncidentAnalysis object
            analysis = IncidentAnalysis(**response_json)

            # 5. Return the object
            return analysis

        except openai.APIError as e:
            raise IncidentAnalysisError(
                "Unable to connect to the LLM provider."
            ) from e

        except JSONDecodeError as e:
            raise IncidentAnalysisError(
                "The AI returned invalid JSON."
            ) from e

        except ValidationError as e:
            raise IncidentAnalysisError(
                "The AI response did not match the expected schema."
            ) from e