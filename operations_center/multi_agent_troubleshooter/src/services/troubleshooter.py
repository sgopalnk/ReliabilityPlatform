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
    TroubleshootingResult,
)

class MultiAgentTroubleshooter:
    """Entry point for multi-agent production troubleshooting."""

    def __init__(self, agents: list[BaseAgent] | None = None) -> None:
        self._coordinator = TroubleshootingCoordinator(
            agents=agents
            if agents is not None
            else [
                CPUAgent(),
                MemoryAgent(),
                NetworkAgent(),
            ]
        )

    def investigate(self, incident: str) -> TroubleshootingResult:
        """Investigate an incident using all configured troubleshooting agents."""

        return self._coordinator.investigate(incident)