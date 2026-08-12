import pytest

from operations_center.multi_agent_troubleshooter.src.agents.base_agent import BaseAgent
from operations_center.multi_agent_troubleshooter.src.models import AgentFinding


class TestAgent(BaseAgent):
    """Minimal concrete agent used to verify the BaseAgent contract."""

    @property
    def name(self) -> str:
        return "Test Agent"

    def investigate(self, incident: str) -> AgentFinding:
        return AgentFinding(
            agent_name=self.name,
            summary=f"Investigated incident: {incident}",
            evidence=[],
            confidence=1.0,
        )


def test_base_agent_requires_implementation() -> None:
    """Verify that BaseAgent cannot be instantiated directly."""
    with pytest.raises(TypeError):
        BaseAgent()


def test_concrete_agent_implements_contract() -> None:
    """Verify that a concrete agent can implement the BaseAgent contract."""
    agent = TestAgent()

    assert agent.name == "Test Agent"

    finding = agent.investigate("Test incident")

    assert isinstance(finding, AgentFinding)
    assert finding.agent_name == "Test Agent"
    assert finding.confidence == 1.0