"""
ReliabilityPlatform ChatOps Assistant

Application entry point.
"""

from chatops_assistant.src.services.chatops_assistant import ChatOpsAssistant


def main():
    """
    Start the ChatOps Assistant.
    """

    assistant = ChatOpsAssistant()
    assistant.start()


if __name__ == "__main__":
    main()