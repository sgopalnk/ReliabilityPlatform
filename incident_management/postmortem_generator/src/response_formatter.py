"""Formatting utilities for Postmortem Generator output."""

from incident_management.postmortem_generator.src.models import Postmortem


def format_postmortem(postmortem: Postmortem) -> str:
    """Format a structured postmortem as readable Markdown."""

    lines = [
        "# Incident Postmortem",
        "",
        "## Incident Summary",
        postmortem.incident_summary,
        "",
        "## Impact",
        postmortem.impact,
        "",
        "## Timeline",
    ]

    for item in postmortem.timeline:
        lines.append(f"- **{item.timestamp}** — {item.event}")
        for evidence in item.evidence:
            lines.append(f"  - Evidence: {evidence}")

    lines.extend(
        [
            "",
            "## Root Cause",
            f"**Status:** {postmortem.root_cause.status}",
            "",
            postmortem.root_cause.statement,
        ]
    )

    if postmortem.root_cause.evidence:
        lines.extend(["", "**Evidence:**"])
        for evidence in postmortem.root_cause.evidence:
            lines.append(f"- {evidence}")

    sections = [
        ("Contributing Factors", postmortem.contributing_factors),
        ("What Went Well", postmortem.what_went_well),
        ("What Went Poorly", postmortem.what_went_poorly),
    ]

    for title, items in sections:
        lines.extend(["", f"## {title}"])
        for item in items:
            lines.append(f"- {item}")

    lines.extend(["", "## Corrective Actions"])
    for item in postmortem.corrective_actions:
        lines.append(f"- **{item.action}** — {item.rationale}")

    lines.extend(["", "## Preventive Actions"])
    for item in postmortem.preventive_actions:
        lines.append(f"- **{item.action}** — {item.rationale}")

    lines.extend(["", "## Lessons Learned"])
    for item in postmortem.lessons_learned:
        lines.append(f"- {item}")

    return "\n".join(lines)
