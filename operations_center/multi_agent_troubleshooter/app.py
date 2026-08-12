import json
import sys

from operations_center.multi_agent_troubleshooter.src.services.troubleshooter import (
    MultiAgentTroubleshooter,
)


def main() -> None:
    """Run the Multi-Agent Troubleshooter from the command line."""

    incident = " ".join(sys.argv[1:]).strip()

    if not incident:
        print("Usage: python -m operations_center.multi_agent_troubleshooter.app <incident>")
        return

    troubleshooter = MultiAgentTroubleshooter()
    result = troubleshooter.investigate(incident)

    print(
        json.dumps(
            result.model_dump(),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()