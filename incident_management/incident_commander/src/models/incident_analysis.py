from threading import activeCount

from pydantic import BaseModel

#Domain model
class IncidentAnalysis(BaseModel):
    executive_summary: str
    possible_root_cause: str
    confidence_level: str
    immediate_actions: list[str]
    business_impact: str

    def to_text(self) -> str:
        """
        Returns a nicely formatted report.
        :return:
        """

        actions = "\n".join(
            f" - {action}"
            for action in self.immediate_actions
        )

        return f"""
==================================================
              AI INCIDENT COMMANDER
==================================================

Executive Summary
--------------------------------------------------
{self.executive_summary}

Possible Root Cause
--------------------------------------------------
{self.possible_root_cause}

Confidence Level
--------------------------------------------------
{self.confidence_level}

Immediate Actions
--------------------------------------------------
{actions}

Business Impact
--------------------------------------------------
{self.business_impact}
""".strip()