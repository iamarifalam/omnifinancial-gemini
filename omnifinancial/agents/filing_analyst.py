"""
SEC 10-K & Regulatory Risk Agent: Analyzes long-context text & notes for material disclosures.
"""

from typing import List
from omnifinancial.models.financial_filing import CorporateFilingSubmission, AgentFinding
from omnifinancial.agents.base import BaseFinancialAgent


class SECFilingAnalystAgent(BaseFinancialAgent):
    def __init__(self):
        super().__init__(
            name="SECFilingAnalystAgent",
            focus_domain="SEC 10-K / 10-Q Disclosures, Risk Factors & Notes to Financials",
        )

    async def analyze(self, filing: CorporateFilingSubmission) -> List[AgentFinding]:
        findings: List[AgentFinding] = []

        for section in filing.sections:
            content_lower = section.content.lower()
            page_ref = section.page_numbers[0] if section.page_numbers else 1

            # 1. Going Concern / Liquidity Warning
            if any(k in content_lower for k in ["substantial doubt", "going concern", "inability to meet obligations"]):
                findings.append(
                    AgentFinding(
                        agent_name=self.name,
                        finding_title="Material Going-Concern / Liquidity Deficiency Warning",
                        severity="HIGH",
                        confidence=0.96,
                        cited_page=page_ref,
                        section_reference=section.item_id,
                        narrative="Management explicitly notes substantial doubts regarding operational solvency over the next 12 months.",
                        evidence_quote=section.content[:240],
                    )
                )

            # 2. Material Regulatory or Litigation Exposure
            if any(k in content_lower for k in ["sec investigation", "subpoena", "department of justice", "formal inquiry", "material litigation"]):
                findings.append(
                    AgentFinding(
                        agent_name=self.name,
                        finding_title="Active Federal Regulatory Investigation or Material Subpoena",
                        severity="HIGH",
                        confidence=0.94,
                        cited_page=page_ref,
                        section_reference=section.item_id,
                        narrative="Disclosed active investigation by regulatory authorities that may impose significant financial sanctions or structural remedies.",
                        evidence_quote=section.content[:240],
                    )
                )

            # 3. Off-Balance Sheet Obligations or Debt Covenant Breach
            if any(k in content_lower for k in ["covenant breach", "default under credit facility", "off-balance sheet arrangement"]):
                findings.append(
                    AgentFinding(
                        agent_name=self.name,
                        finding_title="Debt Covenant Violation or Complex Structured Liabilities",
                        severity="MEDIUM",
                        confidence=0.91,
                        cited_page=page_ref,
                        section_reference=section.item_id,
                        narrative="Credit facility covenant metrics breached or heavy reliance on off-balance sheet SPVs detected.",
                        evidence_quote=section.content[:240],
                    )
                )

        # Baseline positive finding if no critical red flags detected
        if not findings:
            findings.append(
                AgentFinding(
                    agent_name=self.name,
                    finding_title="Clean Unqualified Regulatory Disclosure",
                    severity="POSITIVE",
                    confidence=0.93,
                    cited_page=1,
                    section_reference="Item 1A / Item 7",
                    narrative="Statutory disclosures follow regular operational parameters with standard boilerplate industry risk factors.",
                    evidence_quote="No abnormal litigation, going-concern statements, or covenant breaches observed in filed sections.",
                )
            )

        return findings
