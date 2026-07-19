"""
generate_enriched_csv.py
========================
Reads the raw xlsx dataset, appends the 12 enrichment records
documented in data/data_enrichment_log.md, and writes:

    data/processed/ethiopia_fi_unified_data.csv   — CSV export of raw data
    data/processed/ethiopia_fi_enriched.csv       — raw + enrichment records

Usage:
    python scripts/generate_enriched_csv.py
"""

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).parent.parent
RAW_XLSX = ROOT / "data" / "raw" / "ethiopia_fi_unified_data.xlsx"
PROCESSED_DIR = ROOT / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# 1. Load raw data
# ---------------------------------------------------------------------------
try:
    df_raw = pd.read_excel(RAW_XLSX)
except FileNotFoundError:
    # Fallback: try old location
    df_raw = pd.read_excel(ROOT / "data" / "ethiopia_fi_unified_data.xlsx")

# Normalise column names
df_raw.columns = [c.strip() for c in df_raw.columns]

# Export clean CSV of the base data
csv_base = PROCESSED_DIR / "ethiopia_fi_unified_data.csv"
df_raw.to_csv(csv_base, index=False)
print(f"[✓] Wrote base CSV → {csv_base}  ({len(df_raw)} records)")

# ---------------------------------------------------------------------------
# 2. Build enrichment records
#    All 12 records from data/data_enrichment_log.md (Batch 1)
# ---------------------------------------------------------------------------

COLLECTED_BY = "Abigiya_Trainee"
COLLECTION_DATE = "2025-07-19"

enrichment_rows = [
    # ENC_0001 — ACC_OWNERSHIP 2011
    {
        "record_id": "ENC_0001", "record_type": "observation", "category": None,
        "pillar": "ACCESS", "indicator": "Account Ownership Rate",
        "indicator_code": "ACC_OWNERSHIP", "indicator_direction": "higher_better",
        "value_numeric": 22.0, "value_text": None, "value_type": "percentage", "unit": "%",
        "observation_date": "2011-12-31", "period_start": None, "period_end": None,
        "fiscal_year": "2011", "gender": "all", "location": "national", "region": None,
        "source_name": "Global Findex 2011", "source_type": "survey",
        "source_url": "https://www.worldbank.org/en/publication/globalfindex/report2011",
        "confidence": "high",
        "related_indicator": None, "relationship_type": None,
        "impact_direction": None, "impact_magnitude": None,
        "impact_estimate": None, "lag_months": None, "evidence_basis": None,
        "comparable_country": None,
        "collected_by": COLLECTED_BY, "collection_date": COLLECTION_DATE,
        "original_text": (
            "22% of Ethiopian adults (age 15+) reported having an account "
            "at a financial institution (Global Findex 2011)."
        ),
        "notes": "Earliest Findex wave; extends time series back to 2011 for trajectory analysis.",
    },
    # ENC_0002 — USG_MM_ACTIVE_RATE 2024
    {
        "record_id": "ENC_0002", "record_type": "observation", "category": None,
        "pillar": "USAGE", "indicator": "Mobile Money Active User Rate",
        "indicator_code": "USG_MM_ACTIVE_RATE", "indicator_direction": "higher_better",
        "value_numeric": 30.5, "value_text": None, "value_type": "percentage",
        "unit": "% of registered users",
        "observation_date": "2024-06-30", "period_start": None, "period_end": None,
        "fiscal_year": "FY2023/24", "gender": "all", "location": "national", "region": None,
        "source_name": "NBE Annual Report FY2023/24", "source_type": "regulator",
        "source_url": "https://nbebank.com/annual-reports/",
        "confidence": "medium",
        "related_indicator": None, "relationship_type": None,
        "impact_direction": None, "impact_magnitude": None,
        "impact_estimate": None, "lag_months": None, "evidence_basis": None,
        "comparable_country": None,
        "collected_by": COLLECTED_BY, "collection_date": COLLECTION_DATE,
        "original_text": (
            "Approximately 30.5% of registered mobile money accounts were active "
            "(at least one transaction in the past 90 days) as of June 2024."
        ),
        "notes": "Quantifies the registered-vs-active gap; explains why Findex account ownership grew only 3 pp despite Telebirr's 40M+ subscribers.",
    },
    # ENC_0003 — ACC_AGENT_COUNT 2024
    {
        "record_id": "ENC_0003", "record_type": "observation", "category": None,
        "pillar": "ACCESS", "indicator": "Mobile Money Agent Network Count",
        "indicator_code": "ACC_AGENT_COUNT", "indicator_direction": "higher_better",
        "value_numeric": 750000, "value_text": None, "value_type": "count", "unit": "agents",
        "observation_date": "2024-06-30", "period_start": None, "period_end": None,
        "fiscal_year": "FY2023/24", "gender": "all", "location": "national", "region": None,
        "source_name": "NBE Payment System Report FY2023/24", "source_type": "regulator",
        "source_url": "https://nbebank.com/payment-system-reports/",
        "confidence": "medium",
        "related_indicator": None, "relationship_type": None,
        "impact_direction": None, "impact_magnitude": None,
        "impact_estimate": None, "lag_months": None, "evidence_basis": None,
        "comparable_country": None,
        "collected_by": COLLECTED_BY, "collection_date": COLLECTION_DATE,
        "original_text": (
            "Total licensed mobile money agents reached approximately 750,000 by end of FY2023/24."
        ),
        "notes": "Agent network size is a primary driver of physical access to financial services in rural Ethiopia.",
    },
    # ENC_0004 — Event: NBE Tiered KYC Directive
    {
        "record_id": "ENC_0004", "record_type": "event", "category": "regulation",
        "pillar": None, "indicator": "NBE Tiered KYC Account Directive",
        "indicator_code": "EVT_KYC_TIERED", "indicator_direction": None,
        "value_numeric": None, "value_text": None, "value_type": None, "unit": None,
        "observation_date": "2023-03-01", "period_start": None, "period_end": None,
        "fiscal_year": "2023", "gender": None, "location": None, "region": None,
        "source_name": "National Bank of Ethiopia", "source_type": "regulator",
        "source_url": "https://nbebank.com/directives/",
        "confidence": "high",
        "related_indicator": None, "relationship_type": None,
        "impact_direction": None, "impact_magnitude": None,
        "impact_estimate": None, "lag_months": None, "evidence_basis": None,
        "comparable_country": None,
        "collected_by": COLLECTED_BY, "collection_date": COLLECTION_DATE,
        "original_text": (
            "NBE issued Directive No. FIS/NBE/01/2023 establishing three tiers of simplified "
            "KYC for mobile money accounts, with Tier 1 requiring only a phone number and "
            "national ID or local ID equivalent."
        ),
        "notes": "Regulatory unlock for mass-market mobile money adoption; pillar deliberately empty per schema design.",
    },
    # ENC_0005 — impact_link: Telebirr → ACCESS / ACC_OWNERSHIP
    {
        "record_id": "ENC_0005", "record_type": "impact_link", "category": None,
        "pillar": "ACCESS", "indicator": None, "indicator_code": None,
        "indicator_direction": None,
        "value_numeric": None, "value_text": None, "value_type": None, "unit": None,
        "observation_date": None, "period_start": None, "period_end": None,
        "fiscal_year": None, "gender": None, "location": None, "region": None,
        "source_name": "Ethio Telecom Annual Report", "source_type": "operator",
        "source_url": "https://www.ethiotelecom.et/telebirr/",
        "confidence": "high",
        "related_indicator": "ACC_OWNERSHIP", "relationship_type": "direct",
        "impact_direction": "increase", "impact_magnitude": "high",
        "impact_estimate": None, "lag_months": 6, "evidence_basis": "empirical",
        "comparable_country": None,
        "collected_by": COLLECTED_BY, "collection_date": COLLECTION_DATE,
        "original_text": None,
        "notes": "Telebirr launched May 2021; direct positive impact on account ownership via mobile money onboarding. parent_id=EVT_0001",
    },
    # ENC_0006 — impact_link: Telebirr → USAGE / USG_P2P_COUNT
    {
        "record_id": "ENC_0006", "record_type": "impact_link", "category": None,
        "pillar": "USAGE", "indicator": None, "indicator_code": None,
        "indicator_direction": None,
        "value_numeric": None, "value_text": None, "value_type": None, "unit": None,
        "observation_date": None, "period_start": None, "period_end": None,
        "fiscal_year": None, "gender": None, "location": None, "region": None,
        "source_name": "EthSwitch Annual Report", "source_type": "operator",
        "source_url": "https://www.ethswitch.com.et/annualreport",
        "confidence": "high",
        "related_indicator": "USG_P2P_COUNT", "relationship_type": "direct",
        "impact_direction": "increase", "impact_magnitude": "high",
        "impact_estimate": None, "lag_months": 3, "evidence_basis": "empirical",
        "comparable_country": None,
        "collected_by": COLLECTED_BY, "collection_date": COLLECTION_DATE,
        "original_text": None,
        "notes": "Telebirr drives P2P volume growth; EthSwitch reports 158% increase FY2024/25. parent_id=EVT_0001",
    },
    # ENC_0007 — impact_link: M-Pesa → ACCESS / ACC_MM_ACCOUNT
    {
        "record_id": "ENC_0007", "record_type": "impact_link", "category": None,
        "pillar": "ACCESS", "indicator": None, "indicator_code": None,
        "indicator_direction": None,
        "value_numeric": None, "value_text": None, "value_type": None, "unit": None,
        "observation_date": None, "period_start": None, "period_end": None,
        "fiscal_year": None, "gender": None, "location": None, "region": None,
        "source_name": "Safaricom Ethiopia", "source_type": "operator",
        "source_url": "https://www.safaricom.et/m-pesa",
        "confidence": "medium",
        "related_indicator": "ACC_MM_ACCOUNT", "relationship_type": "direct",
        "impact_direction": "increase", "impact_magnitude": "medium",
        "impact_estimate": None, "lag_months": 12, "evidence_basis": "literature",
        "comparable_country": "Kenya",
        "collected_by": COLLECTED_BY, "collection_date": COLLECTION_DATE,
        "original_text": None,
        "notes": "M-Pesa entry Aug 2023 contributes to mobile money account rate doubling by 2024. parent_id=EVT_0003",
    },
    # ENC_0008 — impact_link: M-Pesa → USAGE / USG_P2P_COUNT
    {
        "record_id": "ENC_0008", "record_type": "impact_link", "category": None,
        "pillar": "USAGE", "indicator": None, "indicator_code": None,
        "indicator_direction": None,
        "value_numeric": None, "value_text": None, "value_type": None, "unit": None,
        "observation_date": None, "period_start": None, "period_end": None,
        "fiscal_year": None, "gender": None, "location": None, "region": None,
        "source_name": "GSMA State of the Industry Report", "source_type": "research",
        "source_url": "https://www.gsma.com/solutions-and-impact/connectivity-for-good/mobile-for-development/gsma_resources/state-of-the-industry-report-on-mobile-money/",
        "confidence": "medium",
        "related_indicator": "USG_P2P_COUNT", "relationship_type": "enabling",
        "impact_direction": "increase", "impact_magnitude": "medium",
        "impact_estimate": None, "lag_months": 6, "evidence_basis": "literature",
        "comparable_country": "Tanzania",
        "collected_by": COLLECTED_BY, "collection_date": COLLECTION_DATE,
        "original_text": None,
        "notes": "Competition from M-Pesa incentivises Telebirr UX/pricing improvements, enabling USAGE growth. parent_id=EVT_0003",
    },
    # ENC_0009 — impact_link: NFIS-II → ACCESS / ACC_OWNERSHIP
    {
        "record_id": "ENC_0009", "record_type": "impact_link", "category": None,
        "pillar": "ACCESS", "indicator": None, "indicator_code": None,
        "indicator_direction": None,
        "value_numeric": None, "value_text": None, "value_type": None, "unit": None,
        "observation_date": None, "period_start": None, "period_end": None,
        "fiscal_year": None, "gender": None, "location": None, "region": None,
        "source_name": "NBE / NFIS-II Strategy", "source_type": "policy",
        "source_url": "https://nbebank.com/financial-inclusion/nfis-ii/",
        "confidence": "medium",
        "related_indicator": "ACC_OWNERSHIP", "relationship_type": "enabling",
        "impact_direction": "increase", "impact_magnitude": "medium",
        "impact_estimate": None, "lag_months": 24, "evidence_basis": "theoretical",
        "comparable_country": None,
        "collected_by": COLLECTED_BY, "collection_date": COLLECTION_DATE,
        "original_text": None,
        "notes": "NFIS-II sets 70% target by 2025; policy ambition shapes regulatory environment. parent_id=EVT_0009",
    },
    # ENC_0010 — impact_link: Fayda → ACCESS / ACC_FAYDA
    {
        "record_id": "ENC_0010", "record_type": "impact_link", "category": None,
        "pillar": "ACCESS", "indicator": None, "indicator_code": None,
        "indicator_direction": None,
        "value_numeric": None, "value_text": None, "value_type": None, "unit": None,
        "observation_date": None, "period_start": None, "period_end": None,
        "fiscal_year": None, "gender": None, "location": None, "region": None,
        "source_name": "Fayda / NIDP", "source_type": "regulator",
        "source_url": "https://fayda.et/",
        "confidence": "high",
        "related_indicator": "ACC_FAYDA", "relationship_type": "direct",
        "impact_direction": "increase", "impact_magnitude": "high",
        "impact_estimate": None, "lag_months": 0, "evidence_basis": "empirical",
        "comparable_country": None,
        "collected_by": COLLECTED_BY, "collection_date": COLLECTION_DATE,
        "original_text": None,
        "notes": "Fayda rollout directly drives enrollment metric; 8M → 15M in 2024–2025. parent_id=EVT_0004",
    },
    # ENC_0011 — impact_link: Fayda → GENDER / GEN_GAP_ACC
    {
        "record_id": "ENC_0011", "record_type": "impact_link", "category": None,
        "pillar": "GENDER", "indicator": None, "indicator_code": None,
        "indicator_direction": None,
        "value_numeric": None, "value_text": None, "value_type": None, "unit": None,
        "observation_date": None, "period_start": None, "period_end": None,
        "fiscal_year": None, "gender": None, "location": None, "region": None,
        "source_name": "ID4Africa 2025 Conference", "source_type": "research",
        "source_url": "https://id4africa.com/2025/",
        "confidence": "medium",
        "related_indicator": "GEN_GAP_ACC", "relationship_type": "enabling",
        "impact_direction": "decrease", "impact_magnitude": "medium",
        "impact_estimate": None, "lag_months": 18, "evidence_basis": "literature",
        "comparable_country": "Rwanda",
        "collected_by": COLLECTED_BY, "collection_date": COLLECTION_DATE,
        "original_text": None,
        "notes": "Fayda lowers ID barrier disproportionately benefiting women; expected to narrow gender gap. parent_id=EVT_0004",
    },
    # ENC_0012 — impact_link: KYC Tiered Directive → GENDER / GEN_MM_SHARE
    {
        "record_id": "ENC_0012", "record_type": "impact_link", "category": None,
        "pillar": "GENDER", "indicator": None, "indicator_code": None,
        "indicator_direction": None,
        "value_numeric": None, "value_text": None, "value_type": None, "unit": None,
        "observation_date": None, "period_start": None, "period_end": None,
        "fiscal_year": None, "gender": None, "location": None, "region": None,
        "source_name": "NBE / GSMA", "source_type": "regulator",
        "source_url": "https://nbebank.com/directives/",
        "confidence": "medium",
        "related_indicator": "GEN_MM_SHARE", "relationship_type": "enabling",
        "impact_direction": "increase", "impact_magnitude": "medium",
        "impact_estimate": None, "lag_months": 12, "evidence_basis": "literature",
        "comparable_country": "Ghana",
        "collected_by": COLLECTED_BY, "collection_date": COLLECTION_DATE,
        "original_text": None,
        "notes": "Simplified KYC disproportionately benefits women who lack formal proof of address. parent_id=ENC_0004",
    },
]

# ---------------------------------------------------------------------------
# 3. Merge and export
# ---------------------------------------------------------------------------

df_new = pd.DataFrame(enrichment_rows)

# Align columns with the base dataframe
all_cols = list(df_raw.columns)
for col in df_new.columns:
    if col not in all_cols:
        all_cols.append(col)

df_new = df_new.reindex(columns=all_cols)
df_raw_aligned = df_raw.reindex(columns=all_cols)

df_enriched = pd.concat([df_raw_aligned, df_new], ignore_index=True)

csv_enriched = PROCESSED_DIR / "ethiopia_fi_enriched.csv"
df_enriched.to_csv(csv_enriched, index=False)
print(f"[✓] Wrote enriched CSV → {csv_enriched}  ({len(df_enriched)} records)")
print(f"    Base: {len(df_raw)} | Added: {len(df_new)} | Total: {len(df_enriched)}")
print("\nRecord type breakdown:")
print(df_enriched["record_type"].value_counts().to_string())
