"""
AI Incident Commander

Entry point for the application.
Reads an incident file, analyzes it using an LLM,
and prints a structured incident report.
"""

import sys

from incident_management.incident_commander.src.services.incident_analyzer import IncidentAnalyzer
from incident_management.incident_commander.src.exceptions import IncidentAnalysisError

def main():

    if len(sys.argv) != 2:
        print("Usage python app.py <incident_file>")
        return

    file_path = sys.argv[1]

    try:
        with open(file_path, "r") as file:
            incident = file.read()
    except FileNotFoundError:
        print(f"Error: Incident file '{file_path}' not found.")
        return

    analyzer = IncidentAnalyzer()

    try:
        analysis = analyzer.analyze(incident)

        print("\n=== AI Incident Commander ===\n")
        print(analysis.to_text())
    except IncidentAnalysisError as e:
        print(f"\nError : {e}")

if __name__ == "__main__":
    main()