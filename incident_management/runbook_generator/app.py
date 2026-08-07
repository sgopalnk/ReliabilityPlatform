import sys

from incident_management.runbook_generator.src.services.runbook_generator import RunbookGenerator
from incident_management.runbook_generator.src.utils.file_utils import (
    read_text_file,
    write_text_file,
)


def main():

    if len(sys.argv) != 2:
        print("Usage: python -m runbook_generator.app <incident_file>")
        return

    incident_file = sys.argv[1]

    try:
        incident = read_text_file(incident_file)

        generator = RunbookGenerator()
        runbook = generator.generate(incident)

        output_file = "incident_management/runbook_generator/runbooks/payment-service-runbook.md"

        write_text_file(output_file, runbook)

        print(f"Runbook generated successfully: {output_file}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()