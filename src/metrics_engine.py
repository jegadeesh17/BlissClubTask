"""Metrics and SLA Engine for BlissClub Last Mile Operations.

Calculates Delivery Health (Delivered, RTO, Lost), 3-stage SLA TAT funnels
(Warehouse, Handover, Courier Transit), geographic intelligence, and partner scorecards.
"""

import numpy as np
import pandas as pd


def compute_delivery_health(df: pd.DataFrame) -> dict:
    """Calculate overall delivery performance indicators and payment-mode splits."""
    total = len(df)
    status_counts = df["Status"].value_counts().to_dict()

    delivered = status_counts.get("DELIVERED", 0)
    rto = status_counts.get("RTO", 0)
    lost = status_counts.get("LOST", 0)
    not_shipped = status_counts.get("Not Shipped", 0)

    # Breakdown by Order Type
    prepaid_df = df[df["Order Type"] == "PrePaid"]
    cod_df = df[df["Order Type"] == "COD"]

    def get_split(sub_df):
        sub_total = len(sub_df)
        if sub_total == 0:
            return {"total": 0, "delivered_pct": 0, "rto_pct": 0}
        sub_deliv = (sub_df["Status"] == "DELIVERED").sum()
        sub_rto = (sub_df["Status"] == "RTO").sum()
        return {
            "total": int(sub_total),
            "delivered_count": int(sub_deliv),
            "delivered_pct": round((sub_deliv / sub_total) * 100, 2),
            "rto_count": int(sub_rto),
            "rto_pct": round((sub_rto / sub_total) * 100, 2),
        }

    return {
        "total_shipments": total,
        "delivered_count": int(delivered),
        "delivered_rate": round((delivered / total) * 100, 2) if total else 0.0,
        "rto_count": int(rto),
        "rto_rate": round((rto / total) * 100, 2) if total else 0.0,
        "lost_count": int(lost),
        "lost_rate": round((lost / total) * 100, 4) if total else 0.0,
        "not_shipped_count": int(not_shipped),
        "not_shipped_rate": round((not_shipped / total) * 100, 2) if total else 0.0,
        "prepaid_health": get_split(prepaid_df),
        "cod_health": get_split(cod_df),
    }


def compute_sla_funnel(df: pd.DataFrame) -> dict:
    """Calculate Turnaround Times (TAT) and SLA breaches across the 3 lifecycle stages."""
    # Filter to delivered orders with valid dates
    deliv_df = df[df["Status"] == "DELIVERED"].copy()

    # Stage 1: Warehouse Fulfillment TAT (Order Date -> AWB Assignment Time)
    s1_hours = (deliv_df["AWB Assignment Time"] - deliv_df["Order Date"]).dt.total_seconds() / 3600.0
    s1_valid = s1_hours[(s1_hours >= 0) & (s1_hours <= 168)]  # filter anomalies > 7 days

    # Stage 2: Handover / Dispatch Lag (AWB Assignment Time -> Pickup Date)
    s2_hours = (deliv_df["Pickup Date"] - deliv_df["AWB Assignment Time"]).dt.total_seconds() / 3600.0
    s2_valid = s2_hours[(s2_hours >= 0) & (s2_hours <= 168)]

    # Stage 3: Courier In-Transit TAT (Pickup Date -> Delivered Date) in days
    s3_days = (deliv_df["Delivered Date"] - deliv_df["Pickup Date"]).dt.total_seconds() / 86400.0
    s3_valid = s3_days[(s3_days >= 0) & (s3_days <= 30)]

    # Total Click-to-Deliver TAT in days
    total_days = (deliv_df["Delivered Date"] - deliv_df["Order Date"]).dt.total_seconds() / 86400.0
    total_valid = total_days[(total_days >= 0) & (total_days <= 30)]

    def summarize_series(s, unit="hours", breach_thresh=None):
        if len(s) == 0:
            return {"mean": 0, "median": 0, "p90": 0, "breach_pct": 0, "unit": unit}
        mean_val = float(s.mean())
        median_val = float(s.median())
        p90_val = float(np.percentile(s, 90))
        breach_pct = float((s > breach_thresh).sum() / len(s) * 100) if breach_thresh else 0.0
        return {
            "mean": round(mean_val, 2),
            "median": round(median_val, 2),
            "p90": round(p90_val, 2),
            "breach_pct": round(breach_pct, 2),
            "unit": unit,
        }

    return {
        "stage_1_warehouse": summarize_series(s1_valid, unit="hours", breach_thresh=12.0),
        "stage_2_handover": summarize_series(s2_valid, unit="hours", breach_thresh=12.0),
        "stage_3_transit": summarize_series(s3_valid, unit="days", breach_thresh=4.0),
        "total_click_to_deliver": summarize_series(total_valid, unit="days", breach_thresh=5.0),
    }


def compute_zone_metrics(df: pd.DataFrame) -> list[dict]:
    """Aggregate volume, spend, delivery rate, and transit speed by Zone."""
    results = []
    zones = sorted(df["Zone"].unique())

    for z in zones:
        sub = df[df["Zone"] == z]
        total = len(sub)
        deliv = (sub["Status"] == "DELIVERED").sum()
        rto = (sub["Status"] == "RTO").sum()
        spend = float(sub["Total Cost"].sum()) if "Total Cost" in sub.columns else 0.0

        # Transit TAT for delivered
        deliv_sub = sub[sub["Status"] == "DELIVERED"]
        transit_days = (deliv_sub["Delivered Date"] - deliv_sub["Pickup Date"]).dt.total_seconds() / 86400.0
        valid_transit = transit_days[(transit_days >= 0) & (transit_days <= 30)]
        avg_transit = round(float(valid_transit.mean()), 2) if len(valid_transit) else 0.0

        results.append({
            "zone": z,
            "shipments": int(total),
            "volume_share_pct": round((total / len(df)) * 100, 2),
            "delivered_rate": round((deliv / total) * 100, 2) if total else 0.0,
            "rto_rate": round((rto / total) * 100, 2) if total else 0.0,
            "total_spend": round(spend, 2),
            "cost_per_awb": round(spend / total, 2) if total else 0.0,
            "avg_transit_days": avg_transit,
        })

    return results


def compute_geographic_intelligence(df: pd.DataFrame, top_n: int = 10) -> list[dict]:
    """Extract state-level demand, payment mix, and RTO correlation."""
    state_counts = df["Shipping State"].value_counts().head(top_n)
    results = []

    for state, count in state_counts.items():
        sub = df[df["Shipping State"] == state]
        deliv = (sub["Status"] == "DELIVERED").sum()
        rto = (sub["Status"] == "RTO").sum()
        cod = (sub["Order Type"] == "COD").sum()
        spend = float(sub["Total Cost"].sum()) if "Total Cost" in sub.columns else 0.0

        results.append({
            "state": state,
            "shipments": int(count),
            "share_pct": round((count / len(df)) * 100, 2),
            "delivered_rate": round((deliv / count) * 100, 2),
            "rto_rate": round((rto / count) * 100, 2),
            "cod_share_pct": round((cod / count) * 100, 2),
            "total_spend": round(spend, 2),
        })

    return results


def compute_partner_scorecards(df: pd.DataFrame) -> dict:
    """Benchmark Aggregators and individual Couriers on cost, speed, and reliability."""
    def scorecard_for_group(group_col):
        cards = []
        for name, sub in df.groupby(group_col):
            total = len(sub)
            deliv = (sub["Status"] == "DELIVERED").sum()
            rto = (sub["Status"] == "RTO").sum()
            spend = float(sub["Total Cost"].sum()) if "Total Cost" in sub.columns else 0.0

            deliv_sub = sub[sub["Status"] == "DELIVERED"]
            transit = (deliv_sub["Delivered Date"] - deliv_sub["Pickup Date"]).dt.total_seconds() / 86400.0
            valid_transit = transit[(transit >= 0) & (transit <= 30)]
            avg_transit = round(float(valid_transit.mean()), 2) if len(valid_transit) else 0.0

            cards.append({
                "partner": name,
                "shipments": int(total),
                "volume_share_pct": round((total / len(df)) * 100, 2),
                "delivered_rate": round((deliv / total) * 100, 2) if total else 0.0,
                "rto_rate": round((rto / total) * 100, 2) if total else 0.0,
                "total_spend": round(spend, 2),
                "cost_per_awb": round(spend / total, 2) if total else 0.0,
                "avg_transit_days": avg_transit,
            })
        return sorted(cards, key=lambda x: x["shipments"], reverse=True)

    return {
        "aggregators": scorecard_for_group("Courier Aggregator"),
        "couriers": scorecard_for_group("Courier"),
    }
