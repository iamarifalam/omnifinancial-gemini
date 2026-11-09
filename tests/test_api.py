"""
API endpoint tests for OmniFinancial.
"""

import pytest
from httpx import AsyncClient, ASGITransport
from omnifinancial.api.app import app


@pytest.mark.asyncio
async def test_api_health():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "healthy"
        assert "Google Gemini API Developer Competition" in data["competition"]


@pytest.mark.asyncio
async def test_sample_filings_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/sample/filings")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) >= 2


@pytest.mark.asyncio
async def test_audit_endpoint():
    transport = ASGITransport(app=app)
    payload = {
        "ticker": "AAPL",
        "company_name": "Apple Inc.",
        "filing_type": "10-K",
        "fiscal_year": 2025,
        "sections": [
            {
                "item_id": "Item 1A",
                "title": "Risk Factors",
                "content": "Global commercial supply chain operations.",
                "page_numbers": [10],
            }
        ],
        "earnings_transcript": "We achieved strong revenue across services and hardware.",
        "charts": [],
    }
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post("/api/audit/filing", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["ticker"] == "AAPL"
        assert "overall_health_score" in data
        assert "findings" in data
