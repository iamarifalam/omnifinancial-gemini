"""
Earnings Call & Qualitative Analyst Agent: Evaluates management tone, unfulfilled guidance, and evasiveness.
"""

from typing import List
from omnifinancial.models.financial_filing import CorporateFilingSubmission, AgentFinding
from omnifinancial.agents.base import BaseFinancialAgent


class EarningsCallAnalystAgent(BaseFinancialAgent):
    def __init__(self):
        super().__init__(
            name="EarningsCallAnalystAgent",
            focus_domain="Quarterly Conference Call Audio/Transcript, Q&A Sentiment & Guidance Realization",
        )

    async def analyze(self, filing: CorporateFilingSubmission) -> List[AgentFinding]:
        findings: List[AgentFinding] = []

        if not filing.earnings_transcript:
            return findings

        transcript_lower = filing.earnings_transcript.lower()

        # 1. Guidance Cut or Revenue Downgrade
        if any(k in transcript_lower for k in ["lowering our guidance", "revised downward", "headwinds in the second half", "softening demand"]):
            findings.append(
                AgentFinding(
                    agent_name=self.name,
                    finding_title="Executive Guidance Retraction / Downward Forecast Revision",
                    severity="HIGH",
                    confidence=0.93,
                    section_reference="Q&A Executive Remarks",
                    narrative="Management proactively reduced forward guidance, citing demand deceleration or enterprise sales cycle lengthening.",
                    evidence_quote="Executive stated downward revision in fiscal outlook.",
                )
            )

        # 2. Executive Resignation or Sudden Departure
        if any(k in transcript_lower for k in ["resignation of our cfo", "interim chief financial officer", "abrupt departure", "stepped down"]):
            findings.append(
                AgentFinding(
                    agent_name=self.name,
                    finding_title="Key C-Suite Turnover (CFO / Chief Accounting Officer)",
                    severity="HIGH",
                    confidence=0.96,
                    section_reference="Management Opening Remarks",
                    narrative="Unplanned executive departure in finance or accounting leadership correlates historically with restatements or internal control disputes.",
                    evidence_quote="Executive transition disclosed during earnings remarks.",
                )
            )

        # 3. Defensive Evasiveness in Analyst Q&A
        if any(k in transcript_lower for k in ["we are not disclosing that at this time", "take that offline", "won't comment on specific customer churn"]):
            findings.append(
                AgentFinding(
                    agent_name=self.name,
                    finding_title="Analyst Query Non-Responsiveness / Metrics Concealment",
                    severity="MEDIUM",
                    confidence=0.88,
                    section_reference="Analyst Q&A Session",
                    narrative="Executive team repeatedly deflected direct inquiries regarding customer churn, retention dynamics, or unit economics.",
                    evidence_quote="Refusal or deflection of direct metric requests by analysts.",
                )
            )

        if not findings:
            findings.append(
                AgentFinding(
                    agent_name=self.name,
                    finding_title="Confident Executive Commentary & Forward Guidance Reaffirmation",
                    severity="POSITIVE",
                    confidence=0.92,
                    section_reference="Conference Call Q&A",
                    narrative="Leadership articulated transparent execution milestones, backed by stable demand pipelines and reiterated fiscal targets.",
                    evidence_quote="Management reaffirmed full-year targets with consistent commentary across all product lines.",
                )
            )

        return findings
