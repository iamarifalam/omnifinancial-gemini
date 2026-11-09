"""
FastAPI Backend Application for OmniFinancial Multimodal Intelligence Fleet.
"""

from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

from omnifinancial.models.financial_filing import (
    CorporateFilingSubmission,
    MultimodalAuditReport,
    SECFilingSection,
    FinancialChartInput,
)
from omnifinancial.agents.synthesis_fleet import OmniFinancialFleetCoordinator

app = FastAPI(
    title="OmniFinancial: Multimodal Financial & Regulatory Intelligence Fleet",
    description="Autonomous Agent Platform powered by Google Gemini 2.5 Multimodal Architecture",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

coordinator = OmniFinancialFleetCoordinator()
STATIC_DIR = Path(__file__).resolve().parent.parent / "static"


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "OmniFinancial Multimodal Fleet",
        "competition": "Google Gemini API Developer Competition ($1,000,000 Pool)",
        "active_agents": [
            "SECFilingAnalystAgent",
            "MultimodalChartVisionAgent",
            "EarningsCallAnalystAgent",
        ],
    }


@app.post("/api/audit/filing", response_model=MultimodalAuditReport)
async def audit_filing_endpoint(filing: CorporateFilingSubmission):
    try:
        report = await coordinator.run_audit(filing)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/sample/filings")
async def get_sample_filings():
    """Provides pre-configured corporate filing test scenarios."""
    return [
        {
            "id": "clean_titan",
            "label": "AlphaCorp Global (Clean Tech Titan)",
            "ticker": "ALPH",
            "company_name": "AlphaCorp Technologies Inc.",
            "filing_type": "10-K",
            "fiscal_year": 2025,
            "sections": [
                {
                    "item_id": "Item 1A: Risk Factors",
                    "title": "Operational Risks",
                    "content": "Our business is subject to standard competitive dynamics and international currency fluctuations. We maintain an investment-grade balance sheet with zero debt covenant defaults.",
                    "page_numbers": [14],
                },
                {
                    "item_id": "Item 7: MD&A",
                    "title": "Management Discussion & Analysis",
                    "content": "Operating revenue expanded by 24% year-over-year. Cash flow from operations increased in direct parity with operating income.",
                    "page_numbers": [38],
                },
            ],
            "earnings_transcript": "Good morning. We are pleased to report record operating margins of 38%. Demand remains exceptionally strong across all cloud and AI product lines.",
            "charts": [
                {
                    "chart_id": "CHART-01",
                    "chart_type": "BALANCE_SHEET",
                    "title": "Operating Cash Conversion Curve",
                    "key_metrics": {
                        "net_income_usd": 1200000000.0,
                        "operating_cash_flow_usd": 1450000000.0,
                        "debt_to_equity_ratio": 0.45,
                        "gross_margin_pct": 54.0,
                        "previous_gross_margin_pct": 52.0,
                    },
                }
            ],
        },
        {
            "id": "distressed_divergence",
            "label": "Apex Retail (Distressed Accounting Divergence)",
            "ticker": "APEX",
            "company_name": "Apex OmniCommerce Group",
            "filing_type": "10-K",
            "fiscal_year": 2025,
            "sections": [
                {
                    "item_id": "Item 1A: Risk Factors",
                    "title": "Liquidity & Going Concern Notice",
                    "content": "Due to recurring operating deficits and credit facility constraints, there is substantial doubt regarding our ability to continue as a going concern without additional equity restructuring.",
                    "page_numbers": [22],
                },
                {
                    "item_id": "Item 3: Legal Proceedings",
                    "title": "Regulatory Inquiry",
                    "content": "The company received a formal subpoena and SEC investigation regarding revenue recognition practices on deferred multi-year software licenses.",
                    "page_numbers": [49],
                },
            ],
            "earnings_transcript": "We are lowering our guidance for the second half. Regarding analyst questions on customer churn, we are not disclosing that at this time and will take that offline.",
            "charts": [
                {
                    "chart_id": "CHART-02",
                    "chart_type": "CANDLESTICK",
                    "title": "Earnings vs Cash Flow Disconnect",
                    "key_metrics": {
                        "net_income_usd": 45000000.0,
                        "operating_cash_flow_usd": -120000000.0,
                        "debt_to_equity_ratio": 6.8,
                        "gross_margin_pct": 28.0,
                        "previous_gross_margin_pct": 42.0,
                    },
                }
            ],
        },
    ]


@app.get("/")
async def serve_index():
    index_path = STATIC_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return JSONResponse({"message": "OmniFinancial API live. UI index.html not yet placed."})
