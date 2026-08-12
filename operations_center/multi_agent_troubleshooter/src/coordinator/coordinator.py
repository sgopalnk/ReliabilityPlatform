from operations_center.multi_agent_troubleshooter.src.agents.base_agent import (
    BaseAgent,
)
from operations_center.multi_agent_troubleshooter.src.models import AgentFinding


class TroubleshootingCoordinator:
    """Coordinates specialized agents during incident investigation."""

    def __init__(self, agents: list[BaseAgent]) -> None:
        self._agents = agents

    def investigate(self, incident: str) -> list[AgentFinding]:
        """Run all configured agents against the same incident."""

        findings: list[AgentFinding] = []

        for agent in self._agents:
            finding = agent.investigate(incident)
            findings.append(finding)

        return findings