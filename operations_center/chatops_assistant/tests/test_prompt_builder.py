"""
Unit tests for the PromptBuilder.
"""

from operations_center.chatops_assistant.src.prompt_builder import PromptBuilder


def test_build_prompt_contains_question():
    """
    Verify the generated prompt contains the user's question.
    """
    question = "What is MTTR?"

    prompt = PromptBuilder.build(question)

    assert question in prompt