"""
Pydantic Data Models for OmniFinancial Multimodal Agent Fleet.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class FinancialChartInput(BaseModel):
    chart_id: str
    chart_type: str = "CANDLESTICK"  # CANDLESTICK, BALANCE_SHEET, REVENUE_TREND
    title: str
    image_base64: Optional[str] = None
    timeframe: str = "Q3-2024 to Q3-2025"
    key_metrics: Dict[str, float] = Field(default_factory=dict)


class SECFilingSection(BaseModel):
    item_id: str  # e.g., "Item 1A: Risk Factors", "Item 7: MD&A"
    title: str
    content: str
    page_numbers: List[int] = Field(default_factory=list)


class CorporateFilingSubmission(BaseModel):
    ticker: str
    company_name: str
    filing_type: str = "10-K"  # 10-K, 10-Q, 8-K
    fiscal_year: int = 2025
    sections: List[SECFilingSection] = Field(default_factory=list)
    earnings_transcript: Optional[str] = None
    charts: List[FinancialChartInput] = Field(default_factory=list)


class AgentFinding(BaseModel):
    agent_name: str
    finding_title: str
    severity: str  # HIGH, MEDIUM, LOW, POSITIVE
    confidence: float = Field(ge=0.0, le=1.0)
    cited_page: Optional[int] = None
    section_reference: Optional[str] = None
    narrative: str
    evidence_quote: str


class MultimodalAuditReport(BaseModel):
    report_id: str
    ticker: str
    company_name: str
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    executive_summary: str
    overall_health_score: float = Field(ge=0.0, le=100.0)  # 0 to 100
    risk_level: str  # LOW, MODERATE, HIGH, CRITICAL
    findings: List[AgentFinding] = Field(default_factory=list)
    multimodal_insights: Dict[str, Any] = Field(default_factory=dict)
    recommendations: List[str] = Field(default_factory=list)
