# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **M1: Data Loader & Rate Card Cost Engine:**
  - Fast schema normalization with Parquet caching (`src/data_loader.py`).
  - Billable 500g weight slab rounder and exact multi-partner Rate Card pricing (`src/cost_engine.py`).
  - Automated unit test suite verifying pricing across A1, A2, A3 and zones A–F (`tests/test_cost_engine.py`).
- **M2: SLA Funnel & Volume Reallocation Simulator:**
  - 3-stage lifecycle TAT funnel analyzer (Warehouse, Handover, Transit) (`src/metrics_engine.py`).
  - What-if volume reallocation optimizer with capacity risk checks (`src/simulator.py`).
  - Automated unit test suite verifying lead times and simulations (`tests/test_metrics_engine.py`).
  - End-to-end data pipeline exporter (`scripts/export_analytics.py`) serializing 92k shipment metrics to `docs/data/ops_data.json`.
- **M3: GitHub Pages Interactive Dashboard & Executive Strategy Memo:**
  - Interactive, responsive web dashboard (`docs/index.html`) with 6 executive tabs, Tailwind styling, Chart.js visuals, and live volume reallocation slider.
  - Comprehensive, board-ready strategic defense paper (`docs/EXECUTIVE_MEMO.md`) answering all 6 assignment questions with hard numbers and trade-off analyses.
- **Living Documentation:**
  - `docs/SPEC.md`, `docs/ARCHITECTURE.md`, `docs/DECISIONS.md`.

