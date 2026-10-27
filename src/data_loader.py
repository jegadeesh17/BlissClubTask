"""Data loader and normalization module for Last Mile Operations.

Handles fast ingestion, caching to Parquet, column normalization,
and type validation for 92,707 shipment records and courier rate cards.
"""

from pathlib import Path
import pandas as pd
import openpyxl

DEFAULT_DATA_PATH = Path("Assignment - Ops LM (3) (1).xlsx")
CACHE_DIR = Path("data")
CACHE_FILE = CACHE_DIR / "clean_shipments.parquet"

# Exact rate cards parsed from Rate Card sheet
RATE_CARD = {
    "A3": {
        "A": {"base_500g": 24.0, "addnl_500g": 24.0},
        "B": {"base_500g": 27.0, "addnl_500g": 27.0},
        "C": {"base_500g": 33.0, "addnl_500g": 33.0},
        "D": {"base_500g": 39.0, "addnl_500g": 39.0},
        "E": {"base_500g": 56.0, "addnl_500g": 56.0},
        "F": {"base_500g": 56.0, "addnl_500g": 56.0},  # fallback to Zone E
        "cod_flat": 25.0,
        "cod_min_pct": 0.015,
    },
    "A2": {
        "A": {"base_500g": 20.2, "addnl_500g": 20.2},
        "B": {"base_500g": 23.5, "addnl_500g": 22.4},
        "C": {"base_500g": 32.5, "addnl_500g": 28.0},
        "D": {"base_500g": 39.2, "addnl_500g": 31.4},
        "E": {"base_500g": 44.8, "addnl_500g": 40.3},
        "F": {"base_500g": 44.8, "addnl_500g": 40.3},  # fallback to Zone E
        "cod_flat": 28.0,
        "cod_min_pct": 0.0134,
    },
    "A1": {
        "A": {"base_500g": 19.0, "addnl_500g": 18.0},
        "B": {"base_500g": 22.0, "addnl_500g": 21.0},
        "C": {"base_500g": 32.0, "addnl_500g": 29.0},
        "D": {"base_500g": 38.0, "addnl_500g": 34.0},
        "E": {"base_500g": 41.0, "addnl_500g": 37.0},
        "F": {"base_500g": 43.0, "addnl_500g": 34.0},
        "cod_flat": 25.0,
        "cod_min_pct": 0.012,
    },
}


def load_rate_card() -> dict:
    """Return the structured rate card dictionary."""
    return RATE_CARD


def load_shipments(file_path: Path | str = DEFAULT_DATA_PATH, force_reload: bool = False) -> pd.DataFrame:
    """Load shipment data with parquet caching and standardized schema cleaning."""
    file_path = Path(file_path)
    cache_path = CACHE_FILE

    if not force_reload and cache_path.exists():
        df = pd.read_parquet(cache_path)
        return df

    if not file_path.exists():
        raise FileNotFoundError(f"Shipment dataset not found at {file_path}")

    # Load from Excel
    df = pd.read_excel(file_path, sheet_name="Data")

    # Clean column names
    df.columns = [str(c).strip() for c in df.columns]

    # Normalization rules
    # 1. Normalize Status
    df["Status"] = df["Status"].astype(str).str.strip()
    df["Status"] = df["Status"].replace({"Lost": "LOST"})

    # 2. Normalize Zone
    df["Zone"] = df["Zone"].astype(str).str.strip().str.upper()

    # 3. Normalize Aggregator & Courier
    df["Courier Aggregator"] = df["Courier Aggregator"].astype(str).str.strip().str.upper()
    df["Courier"] = df["Courier"].astype(str).str.strip().str.upper()

    # 4. Normalize Order Type
    df["Order Type"] = df["Order Type"].astype(str).str.strip()
    df["Order Type"] = df["Order Type"].replace({"Prepaid": "PrePaid", "prepaid": "PrePaid", "cod": "COD"})

    # 5. Normalize Shipping State
    df["Shipping State"] = df["Shipping State"].astype(str).str.strip().str.title()

    # 6. Parse timestamps
    for date_col in ["Order Date", "AWB Assignment Time", "Pickup Date", "Delivered Date"]:
        if date_col in df.columns:
            df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    # 7. Clean weight
    weight_col = "Shipment weight (in Kg)"
    if weight_col in df.columns:
        df[weight_col] = pd.to_numeric(df[weight_col], errors="coerce")
        df[weight_col] = df[weight_col].fillna(0.5)

    # 8. Ensure string columns with mixed types (numeric vs alphanumeric) are strictly strings
    for col in ["AWB", "Order ID", "Product", "SKU", "Pickup Point", "Shipping pincode"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # Save to parquet cache for future 0.05s loads
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    df.to_parquet(cache_path, index=False)

    return df
