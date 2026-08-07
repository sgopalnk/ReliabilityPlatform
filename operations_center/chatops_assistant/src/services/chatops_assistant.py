"""
ChatOps Assistant

Provides an interactive command-line interface for
ReliabilityPlatform modules.
"""

from core.logger import get_logger

logger = get_logger("chatops_assistant")


class ChatOpsAssistant:
    """
    Interactive command-line assistant for ReliabilityPlatform.
    """

    def start(self):
        """
        Start the interactive ChatOps session.
        """

        logger.info("Starting ChatOps Assistant.")

        print("\n============================================================")
        print("          ReliabilityPlatform ChatOps Assistant")
        print("============================================================")
        print("\nType 'help' to see available commands.\n")

        while True:

            command = input("chatops> ").strip().lower()

            if command == "help":
                self.show_help()

            elif command == "clear":
                self.clear_screen()

            elif command == "exit":
                logger.info("ChatOps Assistant terminated.")
                print("Goodbye!")
                break

            elif command == "":
                continue

            else:
                print("Unknown command. Type 'help'.")

    def show_help(self):
        """
        Display available commands.
        """

        print("\nAvailable Commands")
        print("------------------")
        print("help      Show available commands")
        print("clear     Clear the screen")
        print("exit      Exit ChatOps")
        print()

    def clear_screen(self):
        """
        Clear the terminal screen.
        """

        print("\033c", end="")