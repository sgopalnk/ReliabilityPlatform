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