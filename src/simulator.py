"""Volume Reallocation Simulator for BlissClub Last Mile Operations.

Models what-if financial impact and operational risks of shifting shipment volumes
from Aggregator A3 to Aggregators A1 and A2 across specific zones.
"""

import pandas as pd
from src.cost_engine import apply_cost_engine, load_rate_card


def simulate_reallocation(
    df: pd.DataFrame,
    shift_pct: float = 25.0,
    split_to_a1: float = 0.5,
    target_zones: list[str] = None,
    rate_card: dict = None,
) -> dict:
    """Simulate shifting a percentage of A3 volume to A1 and A2.

    Parameters:
    - shift_pct: Percentage (0 to 100) of A3 volume in target zones to reallocate.
    - split_to_a1: Fraction (0.0 to 1.0) of shifted volume assigned to A1 (remainder to A2).
    - target_zones: List of zones to reallocate from (default: ['A', 'B']).
    """
    if rate_card is None:
        rate_card = load_rate_card()
    if target_zones is None:
        target_zones = ["A", "B"]

    target_zones = [z.upper() for z in target_zones]
    df_sim = df.copy()

    # Identify candidate shipments (A3 shipments in target zones)
    mask = (df_sim["Courier Aggregator"] == "A3") & (df_sim["Zone"].isin(target_zones))
    candidate_indices = df_sim[mask].index.to_numpy()
    total_candidates = len(candidate_indices)

    if total_candidates == 0 or shift_pct <= 0:
        base_cost = float(df_sim["Total Cost"].sum())
        return {
            "shift_pct": shift_pct,
            "reallocated_shipments": 0,
            "baseline_spend": round(base_cost, 2),
            "simulated_spend": round(base_cost, 2),
            "monthly_savings": 0.0,
            "annualized_savings": 0.0,
            "savings_pct": 0.0,
            "partner_volumes": {
                "A1": int((df_sim["Courier Aggregator"] == "A1").sum()),
                "A2": int((df_sim["Courier Aggregator"] == "A2").sum()),
                "A3": int((df_sim["Courier Aggregator"] == "A3").sum()),
            },
            "capacity_risk": "None",
        }

    # Deterministic selection based on shift_pct
    num_to_shift = int(total_candidates * (shift_pct / 100.0))
    shift_indices = candidate_indices[:num_to_shift]

    # Split between A1 and A2
    num_to_a1 = int(num_to_shift * split_to_a1)
    a1_indices = shift_indices[:num_to_a1]
    a2_indices = shift_indices[num_to_a1:]

    # Apply reassignments
    df_sim.loc[a1_indices, "Courier Aggregator"] = "A1"
    df_sim.loc[a2_indices, "Courier Aggregator"] = "A2"

    # Recalculate costs
    df_sim = apply_cost_engine(df_sim, rate_card)

    baseline_spend = float(df["Total Cost"].sum())
    simulated_spend = float(df_sim["Total Cost"].sum())
    monthly_savings = baseline_spend - simulated_spend
    annualized_savings = monthly_savings * 12.0

    # Partner volumes
    vol_a1 = int((df_sim["Courier Aggregator"] == "A1").sum())
    vol_a2 = int((df_sim["Courier Aggregator"] == "A2").sum())
    vol_a3 = int((df_sim["Courier Aggregator"] == "A3").sum())

    base_a1 = int((df["Courier Aggregator"] == "A1").sum())
    base_a2 = int((df["Courier Aggregator"] == "A2").sum())

    # Capacity risk assessment
    growth_a1 = (vol_a1 - base_a1) / base_a1 if base_a1 else 0
    growth_a2 = (vol_a2 - base_a2) / base_a2 if base_a2 else 0

    if growth_a1 > 1.0 or growth_a2 > 1.0:
        capacity_risk = "HIGH (Volume to partner increased by >100%)"
    elif growth_a1 > 0.4 or growth_a2 > 0.4:
        capacity_risk = "MODERATE (Requires phased ramp-up and pickup capacity audit)"
    else:
        capacity_risk = "LOW (Safe operational threshold)"

    return {
        "shift_pct": shift_pct,
        "target_zones": target_zones,
        "reallocated_shipments": num_to_shift,
        "baseline_spend": round(baseline_spend, 2),
        "simulated_spend": round(simulated_spend, 2),
        "monthly_savings": round(monthly_savings, 2),
        "annualized_savings": round(annualized_savings, 2),
        "savings_pct": round((monthly_savings / baseline_spend) * 100, 2),
        "partner_volumes": {
            "A1": vol_a1,
            "A2": vol_a2,
            "A3": vol_a3,
        },
        "volume_deltas": {
            "A1": vol_a1 - base_a1,
            "A2": vol_a2 - base_a2,
            "A3": vol_a3 - int((df["Courier Aggregator"] == "A3").sum()),
        },
        "capacity_risk": capacity_risk,
    }

