# H2C2 — Insight for Impact

**Hacklytics 2026 · Databricks × United Nations**

H2C2 (Humanitarian Health Command Center) is a full-stack intelligence platform that fuses UN Humanitarian Needs Overview (HNO) and Humanitarian Response Plan (HRP) datasets into a single analytical layer — surfacing the funding mismatches, targeting gaps, and future neglect risks that decision-makers miss.

---

## Overview

Every year, billions of dollars in humanitarian aid are allocated without a clear picture of where the need is greatest. Some regions receive generous funding while others — equally devastated — are barely touched. H2C2 closes that gap through four integrated tools:

| Tool | Purpose |
|---|---|
| **Dashboard** | 3D rotating globe with pulsing crisis markers, colored by severity level |
| **Analytics** | Funding intelligence charts measuring the gap between need severity and resources allocated |
| **Forecast** | Two-stage ML pipeline (XGBoost + Prophet) projecting humanitarian needs and funding gaps through 2030 |
| **Genie** | Databricks AI/BI Genie integration — natural language queries over live data, no code required |

---

## Quick Start

### Prerequisites

- Python 3.9+
- Databricks account (for Genie integration in production)

### Installation

```bash
git clone https://github.com/Nikil456/Insight-for-Impact.git
cd Insight-for-Impact
python -m venv venv
source venv/bin/activate      # macOS/Linux
pip install -r requirements.txt
```

### Environment Variables (optional — required for Genie)

Create a `.env` file in the project root:

```
DATABRICKS_HOST=https://<your-workspace>.azuredatabricks.net
DATABRICKS_TOKEN=<your-pat-token>
GENIE_SPACE_ID=<your-genie-space-id>
```

### Run

```bash
streamlit run src/main.py
```

Opens at `http://localhost:8501`.

---

## Project Structure

```
Insight-for-Impact/
├── src/
│   ├── main.py                   # App entry point, navigation, home & dashboard pages
│   ├── analytics_page.py         # Crisis Funding Intelligence page
│   ├── forecast_page.py          # ML Forecast page
│   ├── about_page.py             # About page
│   ├── health_regions.py         # Globe rendering and crisis entity data
│   ├── utils.py                  # Shared data loaders and chart helpers
│   └── styles.py                 # Theme colors and all CSS (dark/light mode)
├── data/
│   ├── hpc_hno_2025.csv                              # UN HNO 2025 source data
│   ├── country_level_summary (1).csv                 # Corrected country-level aggregates
│   ├── humanitarian_analysis_country_metrics.csv     # Mismatch scores, targeting efficiency
│   ├── humanitarian_analysis_sector_benchmarking.csv # Sector-level coverage gaps
│   └── humanitarian-response-plans.csv               # HRP historical records
├── models/
│   ├── forecast_results_2026_2030.csv                # Full forecast table (all countries)
│   └── high_neglect_risk_2026_2030.csv               # High-neglect-risk subset (706 entries)
├── fix_country_summary.py        # Utility script to recompute In Need / Targeted from source
├── home.png                      # Home navigation icon asset
├── requirements.txt
└── README.md
```

---

## Data Pipeline

### Source Correction (`fix_country_summary.py`)

The `country_level_summary` file is derived from `hpc_hno_2025.csv`. The script filters rows where `Cluster = ALL` and `Category` is blank — the top-level aggregate row per country — and writes the correct `In Need` and `Targeted` values back to the summary file. Re-run any time the source data is updated:

```bash
python fix_country_summary.py
```

### Key Engineered Metrics

| Metric | Definition |
|---|---|
| **Need Prevalence** | In Need ÷ Total Population |
| **Budget per PIN** | Revised Requirements (USD) ÷ People in Need |
| **Mismatch Score** | Normalized Need Prevalence − Normalized Budget per PIN |
| **Targeting Efficiency** | People Targeted ÷ People in Need |
| **Severity Quartile** | Countries ranked by Need Prevalence into Low / Medium / High / Critical |

---

## ML Forecast Architecture

### Stage 1 — Funding Trend Forecasting (Prophet)

Facebook Prophet trains an individual time-series model per country on historical `revisedRequirements` data (2000–2025). It generates `Predicted_Funding` for 2026–2030. Due to data sparsity, forecasts were produced for 65 of 165 countries (minimum 3 historical data points required).

### Stage 2 — Needs & Requirements Prediction (XGBoost)

XGBoost predicts `Predicted_In_Need` and `Predicted_Requirements` using engineered features:

- **Dependency Ratio** — In Need ÷ Total Population
- **Population Velocity** — 3-year rolling mean of year-over-year % change in In Need
- **Lagged Requirements** — previous year's `revisedRequirements`
- **Cost Inflation** — year-over-year % change in Cost per Beneficiary

Validation used temporal walk-forward (train ≤ 2019, evaluate 2020–2025).  
RMSE: ~429,852 people (In Need) · ~$773M USD (Requirements)

### Risk Flag

`Risk_Flag = True` when `Predicted_Requirements > 1.15 × Predicted_Funding`.  
**706 country-years** flagged as High Neglect Risk across 2026–2030.

---

## Key Findings

**Sudan** holds the highest Mismatch Score (0.59) — 64% of its 47.5M population is in need, with only ~$1,342 budgeted per person. **Afghanistan** follows at 0.53 with ~$1,174 per person in need, the lowest Budget per PIN among Critical-tier countries.

**Colombia** is the most undertargeted country — response plans reach only 22% of the 9M people in need, leaving 7.1M without a targeting commitment.

**Somalia** receives ~$4,287 per person in need despite Critical severity status — more than any other country — while **Guatemala** (Low severity) receives just ~$335 per PIN, illustrating that funding decisions are partly driven by geopolitical visibility rather than need alone.

---

## Tech Stack

| Layer | Technologies |
|---|---|
| Data & ML Platform | Databricks, Delta Lake, Unity Catalog, AI/BI Genie |
| ML Models | XGBoost, Prophet |
| Frontend | Streamlit, Plotly, globe.gl, Three.js |
| Data Sources | UN HDX, OCHA FTS, HNO/HRP Records 2000–2025 |

---

## License

MIT License — Built for Hacklytics 2026 · Georgia Tech

---

*"People need help. It's time to respond where it matters."*
