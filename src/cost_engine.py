"""Cost Engine for BlissClub Last Mile Operations.

Calculates billable 500g weight slabs, applies multi-partner rate card schedules
(A1, A2, A3 across Zones A-F), computes COD surcharges, and quantifies cost leakages.
"""

import math
import numpy as np
import pandas as pd
from src.data_loader import load_rate_card


def calculate_weight_slabs(weight_kg: float) -> int:
    """Calculate the number of 500g (0.5kg) billing slabs.
    
    Minimum billable slab is 1 (first 500g).
    Weights are rounded UP to the nearest 0.5kg increment.
    """
    if pd.isna(weight_kg) or weight_kg <= 0:
        return 1
    return max(1, math.ceil(round(weight_kg, 4) / 0.5))


def calculate_awb_cost(
    aggregator: str,
    zone: str,
    weight_kg: float,
    order_type: str,
    rate_card: dict = None,
) -> dict:
    """Calculate the complete freight, COD, and total cost for a single AWB."""
    if rate_card is None:
        rate_card = load_rate_card()

    agg = str(aggregator).strip().upper()
    z = str(zone).strip().upper()
    o_type = str(order_type).strip()

    # Fallback to A3 if aggregator not found
    agg_rates = rate_card.get(agg, rate_card["A3"])
    
    # Fallback to Zone E if zone not found in aggregator
    zone_rates = agg_rates.get(z)
    if not zone_rates or not isinstance(zone_rates, dict):
        zone_rates = agg_rates.get("E", {"base_500g": 50.0, "addnl_500g": 50.0})

    slabs = calculate_weight_slabs(weight_kg)
    base_rate = float(zone_rates["base_500g"])
    addnl_rate = float(zone_rates["addnl_500g"])

    base_freight = base_rate
    addnl_freight = (slabs - 1) * addnl_rate
    total_freight = base_freight + addnl_freight

    # COD charge
    is_cod = o_type.upper() == "COD"
    cod_fee = float(agg_rates.get("cod_flat", 25.0)) if is_cod else 0.0

    total_cost = total_freight + cod_fee

    return {
        "billable_slabs": slabs,
        "billable_weight_kg": slabs * 0.5,
        "base_freight": round(base_freight, 2),
        "additional_freight": round(addnl_freight, 2),
        "total_freight": round(total_freight, 2),
        "cod_fee": round(cod_fee, 2),
        "total_cost": round(total_cost, 2),
    }


def apply_cost_engine(df: pd.DataFrame, rate_card: dict = None) -> pd.DataFrame:
    """Vectorized calculation of shipping costs across all AWBs in the DataFrame."""
    if rate_card is None:
        rate_card = load_rate_card()

    df = df.copy()

    # Pre-calculate billable slabs
    weights = df["Shipment weight (in Kg)"].fillna(0.5).values
    slabs = np.maximum(1, np.ceil(np.round(weights, 4) / 0.5)).astype(int)
    df["Billable Slabs"] = slabs
    df["Billable Weight (Kg)"] = slabs * 0.5

    # Look up base and addnl rates
    base_freights = np.zeros(len(df), dtype=float)
    addnl_freights = np.zeros(len(df), dtype=float)
    cod_fees = np.zeros(len(df), dtype=float)

    aggs = df["Courier Aggregator"].str.upper().values
    zones = df["Zone"].str.upper().values
    order_types = df["Order Type"].values

    for i in range(len(df)):
        agg = aggs[i]
        z = zones[i]
        o_type = str(order_types[i]).upper()
        s = slabs[i]

        agg_rates = rate_card.get(agg, rate_card["A3"])
        zone_rates = agg_rates.get(z)
        if not zone_rates or not isinstance(zone_rates, dict):
            zone_rates = agg_rates.get("E", {"base_500g": 50.0, "addnl_500g": 50.0})

        b_rate = zone_rates["base_500g"]
        a_rate = zone_rates["addnl_500g"]

        base_freights[i] = b_rate
        addnl_freights[i] = (s - 1) * a_rate
        if o_type == "COD":
            cod_fees[i] = agg_rates.get("cod_flat", 25.0)

    df["Base Freight"] = np.round(base_freights, 2)
    df["Additional Freight"] = np.round(addnl_freights, 2)
    df["Total Freight"] = np.round(base_freights + addnl_freights, 2)
    df["COD Fee"] = np.round(cod_fees, 2)
    df["Total Cost"] = np.round(df["Total Freight"] + df["COD Fee"], 2)

    return df


def get_cost_summary(df: pd.DataFrame) -> dict:
    """Compute high-level financial summary metrics."""
    total_cost = float(df["Total Cost"].sum())
    total_freight = float(df["Total Freight"].sum())
    total_cod_fees = float(df["COD Fee"].sum())
    total_awbs = len(df)
    
    delivered_mask = df["Status"] == "DELIVERED"
    delivered_count = int(delivered_mask.sum())
    cost_per_delivered = total_cost / delivered_count if delivered_count > 0 else 0.0

    return {
        "total_cost": round(total_cost, 2),
        "total_freight": round(total_freight, 2),
        "total_cod_fees": round(total_cod_fees, 2),
        "total_awbs": total_awbs,
        "cost_per_awb": round(total_cost / total_awbs, 2),
        "cost_per_delivered_order": round(cost_per_delivered, 2),
    }


def calculate_cost_leakage(df: pd.DataFrame, rate_card: dict = None) -> dict:
    """Analyze the financial overpayment caused by routing shipments to A3 instead of A1 or A2."""
    if rate_card is None:
        rate_card = load_rate_card()

    # Filter to A3 shipments
    a3_df = df[df["Courier Aggregator"] == "A3"].copy()
    
    # Calculate what these exact shipments would have cost under A1 and A2
    a1_cost_df = a3_df.copy()
    a1_cost_df["Courier Aggregator"] = "A1"
    a1_cost_df = apply_cost_engine(a1_cost_df, rate_card)

    a2_cost_df = a3_df.copy()
    a2_cost_df["Courier Aggregator"] = "A2"
    a2_cost_df = apply_cost_engine(a2_cost_df, rate_card)

    actual_a3_spend = float(a3_df["Total Cost"].sum())
    hypothetical_a1_spend = float(a1_cost_df["Total Cost"].sum())
    hypothetical_a2_spend = float(a2_cost_df["Total Cost"].sum())

    savings_vs_a1 = actual_a3_spend - hypothetical_a1_spend
    savings_vs_a2 = actual_a3_spend - hypothetical_a2_spend

    return {
        "a3_total_shipments": len(a3_df),
        "actual_a3_spend": round(actual_a3_spend, 2),
        "spend_if_all_a1": round(hypothetical_a1_spend, 2),
        "spend_if_all_a2": round(hypothetical_a2_spend, 2),
        "max_potential_savings_a1": round(savings_vs_a1, 2),
        "potential_savings_a2": round(savings_vs_a2, 2),
        "overpayment_pct_vs_a1": round((savings_vs_a1 / actual_a3_spend) * 100, 2),
    }
