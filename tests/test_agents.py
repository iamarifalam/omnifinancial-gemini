"""
Unit tests for OmniFinancial Multimodal Agent Fleet.
"""

import pytest
from omnifinancial.models.financial_filing import (
    CorporateFilingSubmission,
    SECFilingSection,
    FinancialChartInput,
)
from omnifinancial.agents.filing_analyst import SECFilingAnalystAgent
from omnifinancial.agents.chart_vision_analyst import MultimodalChartVisionAgent
from omnifinancial.agents.earnings_call_analyst import EarningsCallAnalystAgent
from omnifinancial.agents.synthesis_fleet import OmniFinancialFleetCoordinator


@pytest.fixture
def clean_filing():
    return CorporateFilingSubmission(
        ticker="ALPH",
        company_name="AlphaCorp Technologies",
        sections=[
            SECFilingSection(
                item_id="Item 1A",
                title="Risk Factors",
                content="Standard commercial operations subject to general macroeconomic cycles.",
                page_numbers=[12],
            )
        ],
        earnings_transcript="We are pleased to reaffirm our full-year guidance with 25% revenue growth.",
        charts=[
            FinancialChartInput(
                chart_id="C-1",
                title="Cash Conversion",
                key_metrics={
                    "net_income_usd": 100000.0,
                    "operating_cash_flow_usd": 120000.0,
                    "debt_to_equity_ratio": 0.5,
                },
            )
        ],
    )


@pytest.fixture
def distressed_filing():
    return CorporateFilingSubmission(
        ticker="DIST",
        company_name="Distressed Holdings Corp",
        sections=[
            SECFilingSection(
                item_id="Item 1A",
                title="Going Concern",
                content="Due to ongoing credit line defaults, there is substantial doubt regarding our ability to continue as a going concern.",
                page_numbers=[33],
            ),
            SECFilingSection(
                item_id="Item 3",
                title="Legal Proceedings",
                content="The company received a formal subpoena regarding an active SEC investigation into revenue booking.",
                page_numbers=[45],
            ),
        ],
        earnings_transcript="We are lowering our guidance and we won't comment on specific customer churn at this time.",
        charts=[
            FinancialChartInput(
                chart_id="C-2",
                title="Earnings Disconnect",
                key_metrics={
                    "net_income_usd": 50000.0,
                    "operating_cash_flow_usd": -80000.0,
                    "debt_to_equity_ratio": 5.2,
                },
            )
        ],
    )


@pytest.mark.asyncio
async def test_clean_filing_evaluation(clean_filing):
    coordinator = OmniFinancialFleetCoordinator()
    report = await coordinator.run_audit(clean_filing)

    assert report.overall_health_score >= 80.0
    assert report.risk_level == "LOW"
    assert len(report.findings) >= 2


@pytest.mark.asyncio
async def test_distressed_filing_triggers_critical_alert(distressed_filing):
    coordinator = OmniFinancialFleetCoordinator()
    report = await coordinator.run_audit(distressed_filing)

    assert report.risk_level in ["HIGH", "CRITICAL"]
    assert report.overall_health_score <= 50.0
    severities = [f.severity for f in report.findings]
    assert "HIGH" in severities


@pytest.mark.asyncio
async def test_chart_vision_divergence():
    agent = MultimodalChartVisionAgent()
    filing = CorporateFilingSubmission(
        ticker="TEST",
        company_name="Test Corp",
        charts=[
            FinancialChartInput(
                chart_id="C-DIV",
                title="Divergence Test",
                key_metrics={
                    "net_income_usd": 200000.0,
                    "operating_cash_flow_usd": -50000.0,
                    "debt_to_equity_ratio": 4.5,
                },
            )
        ],
    )
    findings = await agent.analyze(filing)
    assert any("Critical Cash Flow Divergence" in f.finding_title for f in findings)
    assert any("Severe Financial Leverage" in f.finding_title for f in findings)


@pytest.mark.asyncio
async def test_earnings_call_guidance_cut():
    agent = EarningsCallAnalystAgent()
    filing = CorporateFilingSubmission(
        ticker="TEST",
        company_name="Test Corp",
        earnings_transcript="We are lowering our guidance for Q4 due to severe softening demand.",
    )
    findings = await agent.analyze(filing)
    assert any("Downward Forecast Revision" in f.finding_title for f in findings)
