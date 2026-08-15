"""Pydantic models for the Postmortem Generator capability."""

from typing import Literal

from pydantic import BaseModel, Field


class TimelineEvent(BaseModel):
    """Represents a significant event in the incident timeline."""

    timestamp: str
    event: str
    evidence: list[str] = Field(default_factory=list)


class RootCause(BaseModel):
    """Represents the incident root cause or current root-cause hypothesis."""

    statement: str
    status: Literal["confirmed", "hypothesis", "unknown"]
    evidence: list[str] = Field(default_factory=list)


class ActionItem(BaseModel):
    """Represents a corrective or preventive postmortem action."""

    action: str
    rationale: str


class Postmortem(BaseModel):
    """Structured contract for an incident postmortem."""

    incident_summary: str
    impact: str
    timeline: list[TimelineEvent]
    root_cause: RootCause
    contributing_factors: list[str]
    what_went_well: list[str]
    what_went_poorly: list[str]
    corrective_actions: list[ActionItem]
    preventive_actions: list[ActionItem]
    lessons_learned: list[str]
