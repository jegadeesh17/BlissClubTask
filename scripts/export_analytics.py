"""Analytics Exporter Script for BlissClub Last Mile Operations.

Executes the complete data pipeline over all 92,707 records, applies the Rate Card
financial engine, computes metrics and SLA funnels, and exports clean, structured
JSON data to docs/data/ops_data.json for the GitHub Pages dashboard.
"""

import json
import datetime
import sys
from pathlib import Path

# Ensure repo root is on sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import pandas as pd

from src.data_loader import load_shipments, load_rate_card
from src.cost_engine import apply_cost_engine, get_cost_summary, calculate_cost_leakage
from src.metrics_engine import (
    compute_delivery_health,
    compute_sla_funnel,
    compute_zone_metrics,
    compute_geographic_intelligence,
    compute_partner_scorecards,
)
from src.simulator import simulate_reallocation

OUTPUT_DIR = Path("docs/data")
OUTPUT_FILE = OUTPUT_DIR / "ops_data.json"


def run_pipeline() -> dict:
    print("1. Ingesting and normalizing shipment data...")
    df = load_shipments()
    print(f"   Loaded {len(df)} shipment records.")

    print("2. Applying Rate Card cost engine...")
    rate_card = load_rate_card()
    df = apply_cost_engine(df, rate_card)

    print("3. Computing Delivery Health & Reliability...")
    health = compute_delivery_health(df)

    print("4. Computing Cost-to-Serve & Financial Leakage...")
    cost_summary = get_cost_summary(df)
    cost_leakage = calculate_cost_leakage(df, rate_card)

    print("5. Computing SLA Funnel & Lead Times...")
    sla_funnel = compute_sla_funnel(df)

    print("6. Computing Geographic Intelligence & Zone Profiles...")
    zones = compute_zone_metrics(df)
    geo_intel = compute_geographic_intelligence(df, top_n=15)

    print("7. Computing Partner Benchmark Scorecards...")
    scorecards = compute_partner_scorecards(df)

    print("8. Generating Volume Reallocation Scenarios...")
    scenarios = {}
    for pct in [10, 20, 25, 30, 40, 50]:
        scenarios[str(pct)] = simulate_reallocation(
            df, shift_pct=pct, split_to_a1=0.5, target_zones=["A", "B"], rate_card=rate_card
        )

    print("9. Generating Daily Temporal Trend...")
    df["Order Day"] = df["Order Date"].dt.strftime("%Y-%m-%d")
    daily_groups = df.groupby("Order Day")
    daily_trend = []
    for day, sub in daily_groups:
        total = len(sub)
        deliv = int((sub["Status"] == "DELIVERED").sum())
        rto = int((sub["Status"] == "RTO").sum())
        daily_trend.append({
            "date": day,
            "orders": total,
            "delivered": deliv,
            "rto": rto,
            "rto_rate": round((rto / total) * 100, 2) if total else 0,
        })
    daily_trend = sorted(daily_trend, key=lambda x: x["date"])

    # Weight distribution
    weights = df["Shipment weight (in Kg)"].fillna(0.5)
    under_500g = int((weights <= 0.5).sum())
    over_500g = int((weights > 0.5).sum())

    analytics_payload = {
        "metadata": {
            "generated_at": datetime.datetime.now().isoformat(),
            "total_records": len(df),
            "date_range": {
                "start": str(df["Order Date"].min()),
                "end": str(df["Order Date"].max()),
            },
        },
        "delivery_health": health,
        "cost_summary": cost_summary,
        "cost_leakage": cost_leakage,
        "sla_funnel": sla_funnel,
        "zone_breakdown": zones,
        "geographic_intelligence": geo_intel,
        "weight_distribution": {
            "under_500g_count": under_500g,
            "under_500g_pct": round((under_500g / len(df)) * 100, 2),
            "over_500g_count": over_500g,
            "over_500g_pct": round((over_500g / len(df)) * 100, 2),
        },
        "partner_scorecards": scorecards,
        "reallocation_scenarios": scenarios,
        "daily_trend": daily_trend,
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(analytics_payload, f, indent=2)

    print(f"Successfully exported analytics to {OUTPUT_FILE} ({OUTPUT_FILE.stat().st_size / 1024:.1f} KB)")
    return analytics_payload


if __name__ == "__main__":
    run_pipeline()
