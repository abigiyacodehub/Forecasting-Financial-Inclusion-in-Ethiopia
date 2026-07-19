"""
schema_utils.py
===============
Utilities for working with the unified Ethiopia FI schema:
validation, schema documentation, and record construction helpers.
"""

import pandas as pd
from datetime import date


# ---------------------------------------------------------------------------
# Schema constants
# ---------------------------------------------------------------------------

RECORD_TYPES = {"observation", "event", "impact_link", "target", "baseline", "forecast"}

PILLARS = {"ACCESS", "USAGE", "QUALITY", "AFFORDABILITY", "TRUST", "DEPTH", "GENDER"}

EVENT_CATEGORIES = {
    "product_launch", "market_entry", "market_exit",
    "policy", "regulation", "infrastructure",
    "partnership", "milestone", "economic", "pricing",
}

SOURCE_TYPES = {
    "survey", "operator", "regulator", "research",
    "policy", "news", "calculated", "field",
}

CONFIDENCE_LEVELS = {"high", "medium", "low", "estimated"}

RELATIONSHIP_TYPES = {"direct", "indirect", "enabling", "constraining"}

IMPACT_DIRECTIONS = {"increase", "decrease", "stabilize", "mixed"}

IMPACT_MAGNITUDES = {"high", "medium", "low", "negligible"}

EVIDENCE_BASES = {"empirical", "literature", "theoretical", "expert"}

GENDERS = {"all", "male", "female"}

LOCATIONS = {"national", "urban", "rural"}

# Columns that must NOT be set for events (pillar) or observations (category)
PILLAR_REQUIRED_FOR = {"observation", "target", "impact_link"}
PILLAR_FORBIDDEN_FOR = {"event"}
CATEGORY_REQUIRED_FOR = {"event"}
CATEGORY_FORBIDDEN_FOR = {"observation", "target"}


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_record(record: dict) -> list[str]:
    """Validate a single record dict against the unified schema.

    Parameters
    ----------
    record : dict
        A dictionary representing one data record.

    Returns
    -------
    list[str]
        A list of validation error messages.  Empty list means valid.
    """
    errors: list[str] = []
    rec_type = record.get("record_type", "")

    # record_type
    if rec_type not in RECORD_TYPES:
        errors.append(f"Invalid record_type '{rec_type}'. Must be one of {RECORD_TYPES}.")

    # pillar rules
    pillar = record.get("pillar")
    if rec_type in PILLAR_REQUIRED_FOR and not pillar:
        errors.append(f"'pillar' is required for record_type='{rec_type}'.")
    if rec_type in PILLAR_FORBIDDEN_FOR and pillar:
        errors.append(
            f"'pillar' must be empty for record_type='{rec_type}' "
            f"(found '{pillar}'). Pillar is captured in impact_links."
        )
    if pillar and pillar not in PILLARS:
        errors.append(f"Invalid pillar '{pillar}'. Must be one of {PILLARS}.")

    # category rules
    category = record.get("category")
    if rec_type in CATEGORY_REQUIRED_FOR and not category:
        errors.append(f"'category' is required for record_type='{rec_type}'.")
    if rec_type in CATEGORY_FORBIDDEN_FOR and category:
        errors.append(f"'category' must be empty for record_type='{rec_type}'.")
    if category and category not in EVENT_CATEGORIES:
        errors.append(f"Invalid category '{category}'. Must be one of {EVENT_CATEGORIES}.")

    # confidence
    conf = record.get("confidence")
    if conf and conf not in CONFIDENCE_LEVELS:
        errors.append(f"Invalid confidence '{conf}'.")

    # source_type
    st = record.get("source_type")
    if st and st not in SOURCE_TYPES:
        errors.append(f"Invalid source_type '{st}'.")

    # impact_link-specific
    if rec_type == "impact_link":
        if not record.get("parent_id"):
            errors.append("impact_link records must have a 'parent_id' (the event record_id).")
        rt = record.get("relationship_type")
        if rt and rt not in RELATIONSHIP_TYPES:
            errors.append(f"Invalid relationship_type '{rt}'.")
        imp_dir = record.get("impact_direction")
        if imp_dir and imp_dir not in IMPACT_DIRECTIONS:
            errors.append(f"Invalid impact_direction '{imp_dir}'.")
        imp_mag = record.get("impact_magnitude")
        if imp_mag and imp_mag not in IMPACT_MAGNITUDES:
            errors.append(f"Invalid impact_magnitude '{imp_mag}'.")

    return errors


def validate_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Validate all rows in a DataFrame.

    Returns
    -------
    pd.DataFrame
        DataFrame with an extra column ``validation_errors`` (empty string = valid).
    """
    result = df.copy()
    result["validation_errors"] = df.apply(
        lambda row: "; ".join(validate_record(row.to_dict())), axis=1
    )
    return result


# ---------------------------------------------------------------------------
# Record constructors
# ---------------------------------------------------------------------------

def make_observation(
    record_id: str,
    pillar: str,
    indicator: str,
    indicator_code: str,
    value_numeric: float,
    unit: str,
    observation_date: str,
    fiscal_year: str,
    gender: str,
    location: str,
    source_name: str,
    source_type: str,
    source_url: str,
    confidence: str,
    collected_by: str,
    collection_date: str,
    original_text: str = "",
    notes: str = "",
    indicator_direction: str = "higher_better",
    value_type: str = "percentage",
) -> dict:
    """Construct a valid observation record dictionary."""
    record = {
        "record_id": record_id,
        "record_type": "observation",
        "category": "",
        "pillar": pillar.upper(),
        "indicator": indicator,
        "indicator_code": indicator_code,
        "indicator_direction": indicator_direction,
        "value_numeric": value_numeric,
        "value_text": "",
        "value_type": value_type,
        "unit": unit,
        "observation_date": observation_date,
        "fiscal_year": fiscal_year,
        "gender": gender,
        "location": location,
        "source_name": source_name,
        "source_type": source_type,
        "source_url": source_url,
        "confidence": confidence,
        "collected_by": collected_by,
        "collection_date": collection_date,
        "original_text": original_text,
        "notes": notes,
    }
    errors = validate_record(record)
    if errors:
        raise ValueError(f"Record {record_id} invalid: {errors}")
    return record


def make_event(
    record_id: str,
    category: str,
    indicator: str,
    indicator_code: str,
    observation_date: str,
    source_name: str,
    source_type: str,
    source_url: str,
    confidence: str,
    collected_by: str,
    collection_date: str,
    original_text: str = "",
    notes: str = "",
    fiscal_year: str = "",
) -> dict:
    """Construct a valid event record dictionary (pillar must be empty)."""
    record = {
        "record_id": record_id,
        "record_type": "event",
        "category": category,
        "pillar": "",           # MUST be empty for events
        "indicator": indicator,
        "indicator_code": indicator_code,
        "observation_date": observation_date,
        "fiscal_year": fiscal_year,
        "source_name": source_name,
        "source_type": source_type,
        "source_url": source_url,
        "confidence": confidence,
        "collected_by": collected_by,
        "collection_date": collection_date,
        "original_text": original_text,
        "notes": notes,
    }
    errors = validate_record(record)
    if errors:
        raise ValueError(f"Record {record_id} invalid: {errors}")
    return record


def make_impact_link(
    record_id: str,
    parent_id: str,
    pillar: str,
    related_indicator: str,
    relationship_type: str,
    impact_direction: str,
    impact_magnitude: str,
    lag_months: int,
    evidence_basis: str,
    source_name: str,
    source_type: str,
    source_url: str,
    confidence: str,
    collected_by: str,
    collection_date: str,
    notes: str = "",
) -> dict:
    """Construct a valid impact_link record dictionary."""
    record = {
        "record_id": record_id,
        "record_type": "impact_link",
        "parent_id": parent_id,
        "pillar": pillar.upper(),
        "related_indicator": related_indicator,
        "relationship_type": relationship_type,
        "impact_direction": impact_direction,
        "impact_magnitude": impact_magnitude,
        "lag_months": lag_months,
        "evidence_basis": evidence_basis,
        "source_name": source_name,
        "source_type": source_type,
        "source_url": source_url,
        "confidence": confidence,
        "collected_by": collected_by,
        "collection_date": collection_date,
        "notes": notes,
    }
    errors = validate_record(record)
    if errors:
        raise ValueError(f"Record {record_id} invalid: {errors}")
    return record


# ---------------------------------------------------------------------------
# Schema summary helper
# ---------------------------------------------------------------------------

def print_schema_summary(df: pd.DataFrame) -> None:
    """Print a human-readable summary of the dataset schema and contents."""
    print("=" * 60)
    print("ETHIOPIA FINANCIAL INCLUSION — UNIFIED DATA SCHEMA SUMMARY")
    print("=" * 60)
    print(f"\nTotal records : {len(df)}")
    print(f"Columns       : {len(df.columns)}")

    if "record_type" in df.columns:
        print("\nRecord type breakdown:")
        for rt, cnt in df["record_type"].value_counts().items():
            print(f"  {rt:<15} {cnt:>4} records")

    if "pillar" in df.columns:
        print("\nPillar distribution (observations/targets/impact_links):")
        pillar_df = df[df["pillar"].notna() & (df["pillar"] != "")]
        for p, cnt in pillar_df["pillar"].value_counts().items():
            print(f"  {p:<15} {cnt:>4} records")

    if "source_type" in df.columns:
        print("\nSource type distribution:")
        for st, cnt in df["source_type"].value_counts().items():
            print(f"  {st:<15} {cnt:>4} records")

    if "confidence" in df.columns:
        print("\nConfidence distribution:")
        for cf, cnt in df["confidence"].value_counts().items():
            print(f"  {cf:<15} {cnt:>4} records")

    print("=" * 60)
