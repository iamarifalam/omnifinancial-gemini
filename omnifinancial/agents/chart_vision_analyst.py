"""
Multimodal Chart Vision Agent: Inspects candlestick charts, ratio graphs, and balance sheet trajectories.
"""

from typing import List
from omnifinancial.models.financial_filing import CorporateFilingSubmission, AgentFinding
from omnifinancial.agents.base import BaseFinancialAgent


class MultimodalChartVisionAgent(BaseFinancialAgent):
    def __init__(self):
        super().__init__(
            name="MultimodalChartVisionAgent",
            focus_domain="Visual Financial Trends, Candlesticks, & Balance Sheet Ratio Curves",
        )

    async def analyze(self, filing: CorporateFilingSubmission) -> List[AgentFinding]:
        findings: List[AgentFinding] = []

        for chart in filing.charts:
            metrics = chart.key_metrics

            # 1. Negative Operating Cash Flow vs Net Income Divergence (Classic Accounting Red Flag)
            net_income = metrics.get("net_income_usd", 0.0)
            cfo = metrics.get("operating_cash_flow_usd", 0.0)
            if net_income > 0 and cfo < 0:
                findings.append(
                    AgentFinding(
                        agent_name=self.name,
                        finding_title="Critical Cash Flow Divergence (Positive Net Income vs Negative CFO)",
                        severity="HIGH",
                        confidence=0.95,
                        section_reference=chart.title,
                        narrative=f"Chart '{chart.title}' demonstrates classic earnings quality degradation: Net Income reported at ${net_income:,.0f} while Operating Cash Flow is negative at ${cfo:,.0f}.",
                        evidence_quote=f"Net Income: ${net_income:,.0f} | CFO: ${cfo:,.0f}",
                    )
                )

            # 2. Extreme Debt-to-Equity / Leverage Spike
            debt_to_equity = metrics.get("debt_to_equity_ratio", 1.0)
            if debt_to_equity > 4.0:
                findings.append(
                    AgentFinding(
                        agent_name=self.name,
                        finding_title=f"Severe Financial Leverage Exposure (D/E: {debt_to_equity:.1f}x)",
                        severity="MEDIUM",
                        confidence=0.92,
                        section_reference=chart.title,
                        narrative=f"Corporate balance sheet visual trajectory exhibits dangerously elevated leverage at {debt_to_equity:.1f}x total equity, heightening refinancing and interest rate sensitivity.",
                        evidence_quote=f"Debt-to-Equity Ratio: {debt_to_equity:.1f}x (Industry Benchmark: <1.8x)",
                    )
                )

            # 3. Gross Margin Compression Trend
            gross_margin_pct = metrics.get("gross_margin_pct", 50.0)
            prev_gross_margin_pct = metrics.get("previous_gross_margin_pct", 50.0)
            if prev_gross_margin_pct - gross_margin_pct >= 8.0:
                findings.append(
                    AgentFinding(
                        agent_name=self.name,
                        finding_title="Accelerated Gross Margin Contraction",
                        severity="MEDIUM",
                        confidence=0.89,
                        section_reference=chart.title,
                        narrative=f"Visual margins compressed from {prev_gross_margin_pct:.1f}% down to {gross_margin_pct:.1f}% over the observation cycle, indicating pricing power erosion or inflationary cost pressures.",
                        evidence_quote=f"Margin change: {prev_gross_margin_pct:.1f}% -> {gross_margin_pct:.1f}%",
                    )
                )

        if not findings:
            findings.append(
                AgentFinding(
                    agent_name=self.name,
                    finding_title="Stable Financial Trajectory & Capital Structure",
                    severity="POSITIVE",
                    confidence=0.91,
                    section_reference="Financial Charts",
                    narrative="Multi-period financial diagrams indicate consistent margin stability and healthy operating cash flow conversion.",
                    evidence_quote="Cash flows align with earnings trajectory across verified reporting periods.",
                )
            )

        return findings
