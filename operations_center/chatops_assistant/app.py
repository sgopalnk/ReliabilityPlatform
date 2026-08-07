"""
ReliabilityPlatform ChatOps Assistant

Application entry point.
"""

from operations_center.chatops_assistant.src.services.chatops_assistant import (
    ChatOpsAssistant,
)


def main():
    """
    Start the ChatOps Assistant.
    """
    assistant = ChatOpsAssistant()

    question = input("Ask a Reliability Engineering question: ")

    response = assistant.answer(question)

    print("\n=== ChatOps Assistant ===\n")
    print(response.answer)


if __name__ == "__main__":
    main()