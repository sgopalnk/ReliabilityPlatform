from abc import ABC, abstractmethod

from operations_center.multi_agent_troubleshooter.src.models import AgentFinding


class BaseAgent(ABC):
    """ Base contract for all specialized troubleshooting agents."""

    @property
    @abstractmethod
    def name(self) -> str:
        """ Return the unique name of the troubleshooting agent."""
        raise NotImplementedError

    @abstractmethod
    def investigate(self, incident: str) -> AgentFinding:
        """ Investigate an incident and return structured findings."""
        raise NotImplementedError