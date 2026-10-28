# BlissClub Last Mile Operations Intelligence & Decision Suite

An end-to-end data analytics pipeline, rate card financial model, and operations strategy suite built for the **Operations Analyst Intern** assessment at BlissClub.

The system analyzes **92,707 e-commerce shipments** (January 2026) and a 3-partner contracted **Rate Card** (Aggregators A1, A2, A3) to deliver audited answers, root cause diagnostics, and an actionable 90-day agenda across all 6 assignment problems.

---

## Live Interactive Dashboard

The interactive decision dashboard is hosted live on GitHub Pages:
👉 **[Launch Interactive Dashboard](https://jegadeesh17.github.io/BlissClubTask/)**

*(Or view locally by opening `docs/index.html` in any web browser).*

---

## Key Business Revelations from the Audit

| Core Operational Vector | Finding from 92,707 Shipments | Strategic Impact |
|---|---|---|
| **Delivery Health** | **94.94% Gross Delivery Rate** (88,013 delivered, 4,631 RTOs, 21 lost). | Strong baseline, but single courier **C9 handles 62.4% of total volume** via Aggregator A3, posing an acute single-point-of-failure risk. |
| **Cost-to-Serve Leakage** | **₹5,95,193 / month overpayment** on Aggregator A3. | 73% of volume is routed to A3, despite A3 having higher rates across Zones A, B, C, and E. Reallocating volume to A1/A2 unlocks **₹71.4 Lakhs in annualized savings**. |
| **COD Return Skew** | **Prepaid delivers at 99.16% (0.8% RTO)** vs. **COD delivering at 87.65% (12.23% RTO)**. | **COD accounts for 89.9% of all returns in the company**. RTO is fundamentally a payment-mode friction issue. |
| **First-Mile Handover Lag** | Warehouse manifests orders in **median 0.79 hours**, but parcels sit on docks for **mean 15.98 hours (55.1% breaching 12h SLA)**. | The core delay in Click-to-Deliver speed is courier pickup arrival latency, not linehaul transit speed. |

---

## Project Structure

```
BlissClubTask/
├── .gitignore
├── README.md                         # Project overview and run guide
├── CHANGELOG.md                      # Milestone changelog
├── docs/                             # Living documentation suite & GitHub Pages root
│   ├── index.html                    # GitHub Pages interactive web application
│   ├── EXECUTIVE_MEMO.md             # Comprehensive operations strategy report (Q1–Q6)
│   ├── SPEC.md                       # Functional requirements & acceptance criteria
│   ├── ARCHITECTURE.md               # Technical architecture & mathematical formulas
│   ├── DECISIONS.md                  # Architectural Decision Records (ADRs)
│   ├── data/
│   │   └── ops_data.json             # Pre-calculated analytics payload
│   └── README.md                     # Documentation index
├── src/                              # Modular Python engine
│   ├── __init__.py
│   ├── data_loader.py                # Schema normalization & Parquet caching
│   ├── cost_engine.py                # 500g weight slabs & Rate Card pricing formulas
│   ├── metrics_engine.py             # SLA funnels, delivery health & geographic Pareto
│   └── simulator.py                  # What-if volume reallocation optimizer
├── tests/                            # Automated test suite
│   ├── __init__.py
│   ├── test_cost_engine.py           # Unit tests for weight slabs and pricing
│   └── test_metrics_engine.py        # Unit tests for TAT funnels and simulations
└── scripts/                          # Pipeline scripts
    └── export_analytics.py           # End-to-end data pipeline runner & JSON exporter
```

---

## Quick Start & Reproduction

### Prerequisites
- Python 3.11+
- Virtual environment or system Python with `pandas`, `openpyxl`, `pytest`, `pyarrow`.

### 1. Run Automated Test Suite
```bash
pytest tests/ -v
```

### 2. Re-run End-to-End Pipeline & Re-export Analytics
```bash
python scripts/export_analytics.py
```

### 3. Open Interactive Dashboard
Simply double-click `docs/index.html` or run:
```bash
python -m http.server 8000 --directory docs
```
Then navigate to `http://localhost:8000`.

---

## Comprehensive Operations Strategy Report

For the complete strategic report answering all 6 assignment questions in detail, read:
👉 **[`docs/EXECUTIVE_MEMO.md`](docs/EXECUTIVE_MEMO.md)**

