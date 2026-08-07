"""
    The LLM is mocked so the tests do not make real API calls.
"""
from unittest.mock import MagicMock
from incident_management.runbook_generator.src.services.runbook_generator import RunbookGenerator

def test_generate_runbook():
    """
        Verify that the RunbookGenerator delegates
        runbook generation to the LLM client and
        returns the generated output.
    """
    generator = RunbookGenerator()

    # Replace the real LLM call with a fake one.
    generator.llm_client.generate = MagicMock(
        return_value="# Sample Runbook"
    )

    incident = "Database is down."

    result = generator.generate(incident)

    # Verify the returned runbook.
    assert result == "# Sample Runbook"

    # Verify that the LLM client was called exactly once.
    generator.llm_client.generate.assert_called_once()

    #Verify the incident text was included in the prompt.
    called_prompt = generator.llm_client.generate.call_args[0][0]

    assert incident in called_prompt