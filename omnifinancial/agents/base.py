"""
Base class for OmniFinancial Multimodal Agents.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from omnifinancial.models.financial_filing import CorporateFilingSubmission, AgentFinding


class BaseFinancialAgent(ABC):
    def __init__(self, name: str, focus_domain: str):
        self.name = name
        self.focus_domain = focus_domain

    @abstractmethod
    async def analyze(self, filing: CorporateFilingSubmission) -> List[AgentFinding]:
        """Runs domain-specific analysis on multimodal filing inputs."""
        pass
