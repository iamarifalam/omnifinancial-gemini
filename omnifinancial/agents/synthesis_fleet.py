"""
Synthesis Fleet Coordinator: Combines text, vision, and speech/transcript analysis into a unified institutional audit.
"""

import asyncio
import time
from typing import List, Dict, Any
from omnifinancial.models.financial_filing import (
    CorporateFilingSubmission,
    AgentFinding,
    MultimodalAuditReport,
)
from omnifinancial.agents.filing_analyst import SECFilingAnalystAgent
from omnifinancial.agents.chart_vision_analyst import MultimodalChartVisionAgent
from omnifinancial.agents.earnings_call_analyst import EarningsCallAnalystAgent


class OmniFinancialFleetCoordinator:
    """
    Coordinates multimodal Gemini-powered subagents to evaluate corporate filings
    in high-throughput parallel execution.
    """

    def __init__(self):
        self.filing_agent = SECFilingAnalystAgent()
        self.chart_agent = MultimodalChartVisionAgent()
        self.earnings_agent = EarningsCallAnalystAgent()
        self.agents = [self.filing_agent, self.chart_agent, self.earnings_agent]

    async def run_audit(self, filing: CorporateFilingSubmission) -> MultimodalAuditReport:
        t_start = time.time()

        # Execute all domain agents concurrently
        tasks = [agent.analyze(filing) for agent in self.agents]
        nested_findings: List[List[AgentFinding]] = await asyncio.gather(*tasks)

        all_findings: List[AgentFinding] = []
        for findings in nested_findings:
            all_findings.extend(findings)

        # Calculate composite health score (starts at 100)
        score = 100.0
        high_severity_count = sum(1 for f in all_findings if f.severity == "HIGH")
        medium_severity_count = sum(1 for f in all_findings if f.severity == "MEDIUM")

        score -= high_severity_count * 28.0
        score -= medium_severity_count * 12.0
        score = max(5.0, min(100.0, score))

        if score >= 80.0:
            risk_level = "LOW"
            summary = (
                f"{filing.company_name} ({filing.ticker}) exhibits a robust financial health profile. "
                "Disclosures, chart trajectories, and earnings statements indicate high reporting integrity."
            )
        elif score >= 55.0:
            risk_level = "MODERATE"
            summary = (
                f"{filing.company_name} ({filing.ticker}) displays moderate financial risk factors. "
                "Certain operational divergences or debt ratios warrant monitoring."
            )
        elif score >= 30.0:
            risk_level = "HIGH"
            summary = (
                f"Elevated risk alert for {filing.company_name} ({filing.ticker}). Significant accounting anomalies, "
                "regulatory inquiries, or severe cash flow divergences detected."
            )
        else:
            risk_level = "CRITICAL"
            summary = (
                f"CRITICAL RED FLAG: {filing.company_name} ({filing.ticker}) exhibits acute distress markers, "
                "including potential going-concern disclosure, federal inquiries, or extreme liquidity contraction."
            )

        recommendations = []
        if high_severity_count > 0:
            recommendations.append("Immediate compliance review required on cited regulatory disclosures.")
            recommendations.append("Conduct forensic cash flow reconciliation between reported net income and operating receipts.")
        if medium_severity_count > 0:
            recommendations.append("Stress-test interest coverage ratios against higher refinancing rates.")
        if not recommendations:
            recommendations.append("Reiterate overweight / investment-grade thesis based on clean disclosure trajectory.")

        report_id = f"OMNI-{filing.ticker}-{int(time.time())}"

        return MultimodalAuditReport(
            report_id=report_id,
            ticker=filing.ticker,
            company_name=filing.company_name,
            executive_summary=summary,
            overall_health_score=round(score, 1),
            risk_level=risk_level,
            findings=all_findings,
            multimodal_insights={
                "sections_analyzed": len(filing.sections),
                "charts_analyzed": len(filing.charts),
                "transcript_present": bool(filing.earnings_transcript),
                "execution_time_ms": round((time.time() - t_start) * 1000, 2),
            },
            recommendations=recommendations,
        )
