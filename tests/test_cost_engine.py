"""Automated unit tests for Cost Engine and Rate Card calculations."""

import pytest
import pandas as pd
from src.cost_engine import (
    calculate_weight_slabs,
    calculate_awb_cost,
    apply_cost_engine,
    get_cost_summary,
    calculate_cost_leakage,
)
from src.data_loader import load_rate_card, load_shipments


def test_weight_slab_calculations():
    """Verify weight slab increment rules (500g increments rounded up)."""
    assert calculate_weight_slabs(0.1) == 1
    assert calculate_weight_slabs(0.5) == 1
    assert calculate_weight_slabs(0.5001) == 2
    assert calculate_weight_slabs(0.75) == 2
    assert calculate_weight_slabs(1.0) == 2
    assert calculate_weight_slabs(1.01) == 3
    assert calculate_weight_slabs(2.4) == 5
    assert calculate_weight_slabs(0) == 1
    assert calculate_weight_slabs(None) == 1


def test_rate_card_exact_pricing():
    """Verify exact rate card pricing across aggregators, zones, and order types."""
    # A1 Zone A: Base 19.0, Addnl 18.0, COD 25.0
    res_a1_prepaid = calculate_awb_cost("A1", "A", 0.4, "PrePaid")
    assert res_a1_prepaid["billable_slabs"] == 1
    assert res_a1_prepaid["base_freight"] == 19.0
    assert res_a1_prepaid["additional_freight"] == 0.0
    assert res_a1_prepaid["cod_fee"] == 0.0
    assert res_a1_prepaid["total_cost"] == 19.0

    res_a1_cod = calculate_awb_cost("A1", "A", 0.8, "COD")
    assert res_a1_cod["billable_slabs"] == 2
    assert res_a1_cod["base_freight"] == 19.0
    assert res_a1_cod["additional_freight"] == 18.0
    assert res_a1_cod["cod_fee"] == 25.0
    assert res_a1_cod["total_cost"] == 62.0  # 19 + 18 + 25

    # A3 Zone A: Base 24.0, Addnl 24.0, COD 25.0
    res_a3_prepaid = calculate_awb_cost("A3", "A", 0.4, "PrePaid")
    assert res_a3_prepaid["base_freight"] == 24.0
    assert res_a3_prepaid["total_cost"] == 24.0
    # Overpayment in Zone A vs A1:
    assert res_a3_prepaid["total_cost"] - res_a1_prepaid["total_cost"] == 5.0

    # A3 Zone E: Base 56.0 vs A1 Zone E: Base 41.0
    res_a3_zone_e = calculate_awb_cost("A3", "E", 0.5, "PrePaid")
    res_a1_zone_e = calculate_awb_cost("A1", "E", 0.5, "PrePaid")
    assert res_a3_zone_e["base_freight"] == 56.0
    assert res_a1_zone_e["base_freight"] == 41.0
    assert res_a3_zone_e["total_cost"] - res_a1_zone_e["total_cost"] == 15.0

    # A2 Zone A: Base 20.2, Addnl 20.2, COD 28.0
    res_a2_cod = calculate_awb_cost("A2", "A", 0.5, "COD")
    assert res_a2_cod["base_freight"] == 20.2
    assert res_a2_cod["cod_fee"] == 28.0
    assert res_a2_cod["total_cost"] == 48.2


def test_vectorized_cost_engine():
    """Verify that vectorized calculation matches individual calculation."""
    sample_data = pd.DataFrame([
        {"Shipment weight (in Kg)": 0.4, "Courier Aggregator": "A1", "Zone": "A", "Order Type": "PrePaid", "Status": "DELIVERED"},
        {"Shipment weight (in Kg)": 0.8, "Courier Aggregator": "A1", "Zone": "A", "Order Type": "COD", "Status": "DELIVERED"},
        {"Shipment weight (in Kg)": 0.5, "Courier Aggregator": "A3", "Zone": "E", "Order Type": "PrePaid", "Status": "RTO"},
    ])

    df_cost = apply_cost_engine(sample_data)
    assert df_cost.iloc[0]["Total Cost"] == 19.0
    assert df_cost.iloc[1]["Total Cost"] == 62.0
    assert df_cost.iloc[2]["Total Cost"] == 56.0

    summary = get_cost_summary(df_cost)
    assert summary["total_cost"] == 137.0
    assert summary["total_awbs"] == 3
    assert summary["cost_per_delivered_order"] == round(137.0 / 2, 2)


def test_cost_leakage_logic():
    """Verify cost leakage calculation logic."""
    sample_data = pd.DataFrame([
        {"Shipment weight (in Kg)": 0.4, "Courier Aggregator": "A3", "Zone": "A", "Order Type": "PrePaid", "Status": "DELIVERED"},
        {"Shipment weight (in Kg)": 0.5, "Courier Aggregator": "A3", "Zone": "E", "Order Type": "PrePaid", "Status": "DELIVERED"},
    ])
    sample_data = apply_cost_engine(sample_data)
    # A3 spend: 24.0 + 56.0 = 80.0
    # A1 spend: 19.0 + 41.0 = 60.0 -> savings = 20.0
    leakage = calculate_cost_leakage(sample_data)
    assert leakage["actual_a3_spend"] == 80.0
    assert leakage["spend_if_all_a1"] == 60.0
    assert leakage["max_potential_savings_a1"] == 20.0
