"""
data_loader.py
==============
Functions for loading and validating the Ethiopia Financial Inclusion
unified dataset and reference codes.
"""

import pandas as pd
from pathlib import Path
from typing import Optional, Union


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
DATA_DIR = Path(__file__).parent.parent / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------

def load_unified_data(path: Optional[Union[str, Path]] = None) -> pd.DataFrame:
    """Load the unified Ethiopia FI dataset (CSV or XLSX).

    Parameters
    ----------
    path : str or Path, optional
        Explicit path to the data file.  When omitted the function
        searches for the file in standard locations.

    Returns
    -------
    pd.DataFrame
        Raw, unmodified dataset with consistent dtypes.

    Raises
    ------
    FileNotFoundError
        If no data file can be found.
    """
    if path is None:
        candidates = [
            PROCESSED_DIR / "ethiopia_fi_enriched.csv",
            PROCESSED_DIR / "ethiopia_fi_unified_data.csv",
            RAW_DIR / "ethiopia_fi_unified_data.xlsx",
            DATA_DIR / "ethiopia_fi_unified_data.xlsx",
        ]
        for c in candidates:
            if c.exists():
                path = c
                break
        if path is None:
            raise FileNotFoundError(
                "Could not locate the unified data file. "
                f"Searched: {[str(c) for c in candidates]}"
            )

    path = Path(path)
    try:
        if path.suffix == ".csv":
            df = pd.read_csv(path, dtype=str)
        elif path.suffix in {".xlsx", ".xls"}:
            df = pd.read_excel(path, dtype=str)
        else:
            raise ValueError(f"Unsupported file type: {path.suffix}")
    except Exception as exc:
        raise RuntimeError(f"Failed to read {path}: {exc}") from exc

    df = _coerce_types(df)
    return df


def load_reference_codes(path: Optional[Union[str, Path]] = None) -> pd.DataFrame:
    """Load the reference codes lookup table.

    Parameters
    ----------
    path : str or Path, optional
        Explicit path.  Defaults to ``data/raw/reference_codes.xlsx``.

    Returns
    -------
    pd.DataFrame
    """
    if path is None:
        candidates = [
            RAW_DIR / "reference_codes.xlsx",
            DATA_DIR / "reference_codes.xlsx",
        ]
        for c in candidates:
            if c.exists():
                path = c
                break
        if path is None:
            raise FileNotFoundError("reference_codes file not found.")

    path = Path(path)
    try:
        if path.suffix == ".csv":
            return pd.read_csv(path)
        return pd.read_excel(path)
    except Exception as exc:
        raise RuntimeError(f"Failed to read {path}: {exc}") from exc


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _coerce_types(df: pd.DataFrame) -> pd.DataFrame:
    """Cast columns to appropriate dtypes after reading as str."""
    numeric_cols = [
        "value_numeric", "impact_estimate", "lag_months",
        "impact_magnitude_pct",
    ]
    date_cols = [
        "observation_date", "period_start", "period_end", "collection_date",
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    return df


# ---------------------------------------------------------------------------
# Filtered views
# ---------------------------------------------------------------------------

def get_observations(df: pd.DataFrame) -> pd.DataFrame:
    """Return only observation records."""
    return df[df["record_type"] == "observation"].copy()


def get_events(df: pd.DataFrame) -> pd.DataFrame:
    """Return only event records."""
    return df[df["record_type"] == "event"].copy()


def get_impact_links(df: pd.DataFrame) -> pd.DataFrame:
    """Return only impact_link records."""
    return df[df["record_type"] == "impact_link"].copy()


def get_targets(df: pd.DataFrame) -> pd.DataFrame:
    """Return only target records."""
    return df[df["record_type"] == "target"].copy()


def get_by_pillar(df: pd.DataFrame, pillar: str) -> pd.DataFrame:
    """Return records for a specific pillar (case-insensitive)."""
    return df[df["pillar"].str.upper() == pillar.upper()].copy()


def join_events_to_impact_links(df: pd.DataFrame) -> pd.DataFrame:
    """Merge impact_link rows with their parent event rows.

    Returns a DataFrame with one row per impact_link enriched with
    the event's metadata (indicator, category, observation_date).

    Parameters
    ----------
    df : pd.DataFrame
        Full unified dataset.

    Returns
    -------
    pd.DataFrame
    """
    impacts = get_impact_links(df)
    events = get_events(df)[["record_id", "indicator", "category", "observation_date"]].copy()
    events = events.rename(columns={
        "record_id": "parent_id",
        "indicator": "event_name",
        "category": "event_category",
        "observation_date": "event_date",
    })
    merged = impacts.merge(events, on="parent_id", how="left")
    return merged
