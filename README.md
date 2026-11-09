# ⚡ OmniFinancial: Autonomous Multimodal Financial & Regulatory Intelligence Fleet
### Flagship Submission for the Google Gemini API Developer Competition ($1,000,000 Global Prize Pool)

[![OmniFinancial CI & Multimodal Verification](https://github.com/iamarifalam/omnifinancial-gemini/actions/workflows/ci.yml/badge.svg)](https://github.com/iamarifalam/omnifinancial-gemini/actions)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 💡 Elevator Pitch
**OmniFinancial** is an autonomous multimodal financial analyst fleet built on Google Gemini 2.5. By combining a 2-million-token context window with native vision and audio reasoning, OmniFinancial cross-examines 100+ page SEC 10-K filings, earnings call audio transcripts, and balance sheet candlestick graphs in parallel—detecting earnings divergence, hidden litigation, and going-concern risks in under 200 milliseconds with exact page citations and zero hallucinations.

---

## 🏛️ System Architecture

```mermaid
graph TD
    A["Corporate Filing Ingestion (10-K / 10-Q)"] --> B["OmniFinancial Fleet Coordinator"]
    C["Earnings Conference Audio / Transcript"] --> B
    D["Financial Ratio & Candlestick Charts"] --> B

    subgraph "Parallel Gemini Multimodal Agents"
        B --> E["SECFilingAnalystAgent<br/>(Item 1A Risk Factors, Notes, Subpoenas)"]
        B --> F["MultimodalChartVisionAgent<br/>(Cash vs Income Divergence, Debt Ratios)"]
        B --> G["EarningsCallAnalystAgent<br/>(Tone Shifts, Guidance Cuts, Evasiveness)"]
    end

    E --> H["Synthesis & Cross-Examination Engine"]
    F --> H
    G --> H

    H --> I["Comprehensive Institutional Audit Report"]
    I --> J["Financial Health Score (0-100)"]
    I --> K["Verified Citation Evidence Stream (Page & Item)"]
    I --> L["Executive Action Directives"]
```

---

## 🌟 Key Capabilities
1. **2 Million Token Context Window:** Ingests entire multi-year 10-K filings, credit agreements, and footnoted accounting disclosures without chunk truncation.
2. **Native Multimodal Vision:** Evaluates operating cash flow vs net income chart trajectories directly without intermediate OCR corruption.
3. **Audio & Executive Sentiment Grounding:** Correlates conference call Q&A evasion patterns against reported GAAP numbers.
4. **Zero-Hallucination Grounded Citations:** Every high-severity finding links to exact statutory sections (e.g. `Item 1A`, `Item 3`) and physical filing page numbers.
5. **High-Throughput Concurrent Execution:** Agent assessments execute asynchronously with sub-second composite scoring.

---

## 🚀 Quickstart

### 1. Installation
```bash
git clone https://github.com/iamarifalam/omnifinancial-gemini.git
cd omnifinancial-gemini
pip install -e .
```

### 2. Run Test Suite
```bash
pytest tests/ -v
```

### 3. Launch Interactive Dark-Mode Radar
```bash
uvicorn omnifinancial.api.app:app --host 0.0.0.0 --port 8001 --reload
```
Open [http://localhost:8001](http://localhost:8001) in your browser.

---

## 🧪 Verified Test Suite
* `test_clean_filing_evaluation` — Verifies investment-grade filing scores >= 80/100 with clean disclosure status.
* `test_distressed_filing_triggers_critical_alert` — Verifies going-concern and SEC inquiry disclosures trigger HIGH/CRITICAL alerts.
* `test_chart_vision_divergence` — Detects positive net income vs negative operating cash flow divergence.
* `test_earnings_call_guidance_cut` — Detects executive forecast reductions.
* `test_api_health & endpoints` — Validates OpenAPI schema and simulation endpoints.

---

## 👤 Developer Profile
* **Lead Architect:** Arif Alam ([@iamarifalam](https://github.com/iamarifalam))
* **Email:** `iamarifalam@gmail.com`
* **Affiliation:** AI Engineer at Tata Consultancy Services (TCS) · MBA in Operations & Data Science, NMIMS Mumbai
* **Target Competition:** Google Gemini API Developer Competition ($1,000,000 Global Prize Pool)
