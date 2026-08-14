from typing import Literal

from pydantic import BaseModel, Field


class AgentFinding(BaseModel):
    """Structured findings produced by a specialized troubleshooting agent."""

    agent_name: str = Field(
        description="Name of the agent that produced the finding."
    )
    summary: str = Field(
        description="Concise summary of the agent's investigation."
    )
    evidence: list[str] = Field(
        default_factory=list,
        description="Evidence from the incident that supports the finding.",
    )
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Agent confidence in the finding, expressed from 0.0 to 1.0.",
    )


class AgentFailure(BaseModel):
    """Structured failure information from a troubleshooting agent."""

    agent_name: str = Field(
        description="Name of the agent that failed."
    )
    error: str = Field(
        description="Error message produced by the failed agent."
    )


class TroubleshootingResult(BaseModel):
    """Structured result produced by the troubleshooting coordinator."""

    incident: str = Field(
        description="Original incident provided for investigation."
    )
    findings: list[AgentFinding] = Field(
        default_factory=list,
        description="Findings produced by the specialized troubleshooting agents.",
    )
    failures: list[AgentFailure] = Field(
        default_factory=list,
        description="Failures encountered while running troubleshooting agents.",
    )
    status: Literal["completed", "partial", "failed"] = Field(
        description="Overall status of the troubleshooting investigation."
    )


class SynthesisResult(BaseModel):
    """Structured cross-agent synthesis of a troubleshooting investigation."""

    summary: str = Field(
        description="Overall summary of the investigation findings."
    )
    key_findings: list[str] = Field(
        default_factory=list,
        description="Most important findings across the specialized agents.",
    )
    correlations: list[str] = Field(
        default_factory=list,
        description="Relationships or patterns identified across agent findings.",
    )
    conflicts: list[str] = Field(
        default_factory=list,
        description="Conflicting or contradictory findings across agents.",
    )
    root_cause_hypothesis: str = Field(
        description="Evidence-based hypothesis about the likely root cause."
    )
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence in the overall synthesis, expressed from 0.0 to 1.0.",
    )

class TroubleshootingAnalysis(BaseModel):
    """Complete multi-agent troubleshooting analysis."""

    investigation: TroubleshootingResult = Field(
        description="Raw investigation results produced by the troubleshooting coordinator."
    )
    synthesis: SynthesisResult = Field(
        description="Cross-agent synthesis of the investigation findings."
    )
