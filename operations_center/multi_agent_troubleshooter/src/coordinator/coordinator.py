import logging

from core.logger import get_logger

from operations_center.multi_agent_troubleshooter.src.agents.base_agent import (
    BaseAgent,
)
from operations_center.multi_agent_troubleshooter.src.models import (
    AgentFailure,
    AgentFinding,
    TroubleshootingResult,
)

logger: logging.Logger = get_logger(
    "multi_agent_troubleshooter.coordinator"
)


class TroubleshootingCoordinator:
    """Coordinates specialized agents during incident investigation."""

    def __init__(self, agents: list[BaseAgent]) -> None:
        self._agents = agents

    def investigate(self, incident: str) -> TroubleshootingResult:
        """Run all configured agents against the same incident."""

        logger.info(
            "Starting investigation with %d agents.",
            len(self._agents),
        )

        findings: list[AgentFinding] = []
        failures: list[AgentFailure] = []

        for agent in self._agents:
            logger.info(
                "Starting investigation with %s.",
                agent.name,
            )

            try:
                finding = agent.investigate(incident)
                findings.append(finding)

                logger.info(
                    "%s completed successfully.",
                    agent.name,
                )

            except Exception as exc:
                logger.exception(
                    "%s failed during investigation.",
                    agent.name,
                )

                failures.append(
                    AgentFailure(
                        agent_name=agent.name,
                        error=str(exc),
                    )
                )

        if findings and not failures:
            status = "completed"
        elif findings and failures:
            status = "partial"
        else:
            status = "failed"

        logger.info(
            "Investigation completed with status=%s. "
            "Findings=%d, failures=%d.",
            status,
            len(findings),
            len(failures),
        )

        return TroubleshootingResult(
            incident=incident,
            findings=findings,
            failures=failures,
            status=status,
        )
