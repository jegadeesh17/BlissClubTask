"""Automated unit tests for Metrics Engine and Volume Simulator."""

import pytest
import pandas as pd
import numpy as np
from src.metrics_engine import (
    compute_delivery_health,
    compute_sla_funnel,
    compute_zone_metrics,
    compute_partner_scorecards,
)
from src.simulator import simulate_reallocation
from src.cost_engine import apply_cost_engine


@pytest.fixture
def sample_metrics_df():
    """Create a controlled sample DataFrame for metrics verification."""
    data = [
        # Delivered Prepaid A1 Zone A
        {
            "Order ID": 1, "Order Date": pd.Timestamp("2026-01-01 10:00:00"),
            "AWB Assignment Time": pd.Timestamp("2026-01-01 14:00:00"),  # 4h
            "Pickup Date": pd.Timestamp("2026-01-01 18:00:00"),          # 4h
            "Delivered Date": pd.Timestamp("2026-01-02 18:00:00"),       # 1 day
            "Courier Aggregator": "A1", "Courier": "C1", "Zone": "A",
            "Order Type": "PrePaid", "Status": "DELIVERED", "Shipping State": "Maharashtra",
            "Shipment weight (in Kg)": 0.4
        },
        # Delivered COD A3 Zone A (Breached handover: 18h)
        {
            "Order ID": 2, "Order Date": pd.Timestamp("2026-01-02 10:00:00"),
            "AWB Assignment Time": pd.Timestamp("2026-01-02 14:00:00"),  # 4h
            "Pickup Date": pd.Timestamp("2026-01-03 08:00:00"),          # 18h (breach >12h)
            "Delivered Date": pd.Timestamp("2026-01-05 08:00:00"),       # 2 days
            "Courier Aggregator": "A3", "Courier": "C9", "Zone": "A",
            "Order Type": "COD", "Status": "DELIVERED", "Shipping State": "Maharashtra",
            "Shipment weight (in Kg)": 0.4
        },
        # RTO COD A3 Zone B
        {
            "Order ID": 3, "Order Date": pd.Timestamp("2026-01-03 10:00:00"),
            "AWB Assignment Time": pd.Timestamp("2026-01-03 14:00:00"),
            "Pickup Date": pd.Timestamp("2026-01-03 18:00:00"),
            "Delivered Date": pd.NaT,
            "Courier Aggregator": "A3", "Courier": "C9", "Zone": "B",
            "Order Type": "COD", "Status": "RTO", "Shipping State": "Karnataka",
            "Shipment weight (in Kg)": 0.5
        },
        # Lost Prepaid A2 Zone C
        {
            "Order ID": 4, "Order Date": pd.Timestamp("2026-01-04 10:00:00"),
            "AWB Assignment Time": pd.Timestamp("2026-01-04 14:00:00"),
            "Pickup Date": pd.Timestamp("2026-01-04 18:00:00"),
            "Delivered Date": pd.NaT,
            "Courier Aggregator": "A2", "Courier": "C2", "Zone": "C",
            "Order Type": "PrePaid", "Status": "LOST", "Shipping State": "Delhi",
            "Shipment weight (in Kg)": 0.5
        },
    ]
    df = pd.DataFrame(data)
    return apply_cost_engine(df)


def test_delivery_health(sample_metrics_df):
    """Verify delivery, RTO, and loss rate calculations."""
    health = compute_delivery_health(sample_metrics_df)
    assert health["total_shipments"] == 4
    assert health["delivered_count"] == 2
    assert health["delivered_rate"] == 50.0
    assert health["rto_count"] == 1
    assert health["rto_rate"] == 25.0
    assert health["lost_count"] == 1
    assert health["lost_rate"] == 25.0

    # Prepaid: 2 orders (1 delivered, 1 lost) -> 50% delivery, 0% RTO
    assert health["prepaid_health"]["total"] == 2
    assert health["prepaid_health"]["delivered_pct"] == 50.0
    assert health["prepaid_health"]["rto_pct"] == 0.0

    # COD: 2 orders (1 delivered, 1 RTO) -> 50% delivery, 50% RTO
    assert health["cod_health"]["total"] == 2
    assert health["cod_health"]["rto_pct"] == 50.0


def test_sla_funnel(sample_metrics_df):
    """Verify SLA TAT calculations and breach detection."""
    funnel = compute_sla_funnel(sample_metrics_df)
    
    # Stage 1: Warehouse TAT (both took 4 hours)
    assert funnel["stage_1_warehouse"]["mean"] == 4.0
    assert funnel["stage_1_warehouse"]["breach_pct"] == 0.0

    # Stage 2: Handover TAT (order 1 took 4h, order 2 took 18h -> 50% breach >12h)
    assert funnel["stage_2_handover"]["mean"] == 11.0  # (4 + 18) / 2
    assert funnel["stage_2_handover"]["breach_pct"] == 50.0


def test_simulator(sample_metrics_df):
    """Verify volume reallocation simulation and savings calculation."""
    # Order 2 is A3 in Zone A (Cost: 24 base + 25 COD = 49).
    # If shifted to A1: Cost would be 19 base + 25 COD = 44 (savings = 5.0).
    sim = simulate_reallocation(
        sample_metrics_df,
        shift_pct=100.0,
        split_to_a1=1.0,
        target_zones=["A"]
    )
    assert sim["reallocated_shipments"] == 1
    assert sim["monthly_savings"] == 5.0
    assert sim["annualized_savings"] == 60.0
    assert sim["partner_volumes"]["A1"] == 2
    assert sim["partner_volumes"]["A3"] == 1
