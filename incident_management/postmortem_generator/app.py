"""Command-line entry point for the Postmortem Generator capability."""

import sys
from pathlib import Path

from core.logger import get_logger
from incident_management.postmortem_generator.src.response_formatter import (
    format_postmortem,
)
from incident_management.postmortem_generator.src.services.postmortem_generator import (
    PostmortemGenerator,
)

logger = get_logger("postmortem_generator")


def main() -> None:
    """Generate a postmortem from an incident evidence file."""

    if len(sys.argv) != 2:
        print(
            "Usage: python -m incident_management.postmortem_generator.app "
            "<incident_file>"
        )
        raise SystemExit(1)

    incident_file = Path(sys.argv[1])

    if not incident_file.exists():
        logger.error("Incident file not found: %s", incident_file)
        raise SystemExit(f"Incident file not found: {incident_file}")

    incident_evidence = incident_file.read_text(encoding="utf-8")

    generator = PostmortemGenerator()
    postmortem = generator.generate(incident_evidence)

    print(format_postmortem(postmortem))


if __name__ == "__main__":
    main()
