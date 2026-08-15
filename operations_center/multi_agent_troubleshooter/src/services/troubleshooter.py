from operations_center.multi_agent_troubleshooter.src.agents.base_agent import (
    BaseAgent,
)
from operations_center.multi_agent_troubleshooter.src.agents.cpu_agent import CPUAgent
from operations_center.multi_agent_troubleshooter.src.agents.memory_agent import MemoryAgent
from operations_center.multi_agent_troubleshooter.src.agents.network_agent import NetworkAgent
from operations_center.multi_agent_troubleshooter.src.coordinator.coordinator import (
    TroubleshootingCoordinator,
)
from operations_center.multi_agent_troubleshooter.src.models import (
    TroubleshootingAnalysis,
)
from operations_center.multi_agent_troubleshooter.src.services.finding_synthesizer import (
    FindingSynthesizer,
)


class MultiAgentTroubleshooter:
    """Entry point for multi-agent production troubleshooting."""

    def __init__(
        self,
        agents: list[BaseAgent] | None = None,
        synthesizer: FindingSynthesizer | None = None,
    ) -> None:
        self._coordinator = TroubleshootingCoordinator(
            agents=agents
            if agents is not None
            else [
                CPUAgent(),
                MemoryAgent(),
                NetworkAgent(),
            ]
        )
        self._synthesizer = synthesizer or FindingSynthesizer()

    def investigate(self, incident: str) -> TroubleshootingAnalysis:
        """Investigate an incident and synthesize the agent findings."""

        if not incident.strip():
            raise ValueError("Incident description cannot be empty.")

        investigation = self._coordinator.investigate(incident)
        synthesis = self._synthesizer.synthesize(investigation)

        return TroubleshootingAnalysis(
            investigation=investigation,
            synthesis=synthesis,
        )
