"""
generate_enriched_csv.py
========================
Reads the raw xlsx dataset, appends the 12 enrichment records
documented in data/data_enrichment_log.md, and writes:

    data/processed/ethiopia_fi_unified_data.csv   — CSV export of raw data
    data/processed/ethiopia_fi_enriched.csv       — raw + enrichment records

After writing, three automated validation checks connect the enrichment log
to the CSV output:

    1. Row-count check   — base_count + log_record_count == csv_total
    2. ID-presence check — every ENC_XXXX id in the log exists in csv['record_id']
    3. Required-fields check — source_url, confidence, collected_by,
                               collection_date are non-null for all ENC_ rows

Usage:
    python scripts/generate_enriched_csv.py
"""

import re
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).parent.parent
RAW_XLSX = ROOT / "data" / "raw" / "ethiopia_fi_unified_data.xlsx"
ENRICHMENT_LOG = ROOT / "data" / "data_enrichment_log.md"
PROCESSED_DIR = ROOT / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# 0. Parse enrichment log — extract ENC_ IDs for validation
# ---------------------------------------------------------------------------

def parse_log_enc_ids(log_path: Path) -> list[str]:
    """
    Read data_enrichment_log.md and return every ENC_XXXX record_id listed
    in the consolidated table (first column after the header row).

    The consolidated table starts after the line '| record_id  |' and ends
    at the first blank line following the table body. We extract only values
    whose first column matches ^ENC_\\d{4}$.
    """
    text = log_path.read_text(encoding="utf-8")
    # Match all occurrences of ENC_XXXX in the file (robust to formatting changes)
    ids = re.findall(r"\bENC_\d{4}\b", text)
    # De-duplicate while preserving first-seen order
    seen = set()
    unique_ids = []
    for enc_id in ids:
        if enc_id not in seen:
            seen.add(enc_id)
            unique_ids.append(enc_id)
    return unique_ids


log_enc_ids = parse_log_enc_ids(ENRICHMENT_LOG)
print(f"[i] Enrichment log — ENC_ IDs parsed: {len(log_enc_ids)}")
print(f"    IDs: {', '.join(log_enc_ids)}")

# ---------------------------------------------------------------------------
# 1. Load raw data
# ---------------------------------------------------------------------------

try:
    df_raw = pd.read_excel(RAW_XLSX)
except FileNotFoundError:
    df_raw = pd.read_excel(ROOT / "data" / "ethiopia_fi_unified_data.xlsx")

df_raw.columns = [c.strip() for c in df_raw.columns]

csv_base = PROCESSED_DIR / "ethiopia_fi_unified_data.csv"
df_raw.to_csv(csv_base, index=False)
print(f"\n[✓] Wrote base CSV → {csv_base}  ({len(df_raw)} records)")

# ---------------------------------------------------------------------------
# 2. Build enrichment records (mirrors the consolidated log table exactly)
# ---------------------------------------------------------------------------

COLLECTED_BY = "Abigiya_Trainee"
COLLECTION_DATE = "2025-07-19"

enrichment_rows = [
    # ── Observations ──────────────────────────────────────────────────────────
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
        "notes": "Earliest Findex wave; extends time series to 2011 for trajectory analysis.",
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
        "notes": "Quantifies registered-vs-active gap; confirms registration outpaced genuine usage.",
    },
    # ENC_0003 — ACC_AGENT_COUNT 2024
    {
        "record_id": "ENC_0003", "record_type": "observation", "category": None,
        "pillar": "ACCESS", "indicator": "Mobile Money Agent Network Count",
        "indicator_code": "ACC_AGENT_COUNT", "indicator_direction": "higher_better",
        "value_numeric": 750_000, "value_text": None, "value_type": "count", "unit": "agents",
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
            "The total number of licensed mobile money agents reached approximately "
            "750,000 by end of FY2023/24."
        ),
        "notes": "Supply-side access proxy; agent density is a leading indicator of rural outreach.",
    },
    # ── Event ─────────────────────────────────────────────────────────────────
    # ENC_0004 — NBE Tiered KYC Directive
    {
        "record_id": "ENC_0004", "record_type": "event",
        "category": "regulatory", "pillar": None,
        "indicator": None, "indicator_code": None, "indicator_direction": None,
        "value_numeric": None, "value_text": "NBE Directive FIS/01/2023 — Four-Tier KYC Framework",
        "value_type": None, "unit": None,
        "observation_date": "2023-03-01", "period_start": None, "period_end": None,
        "fiscal_year": "FY2022/23", "gender": None, "location": "national", "region": None,
        "source_name": "NBE Directive FIS/01/2023", "source_type": "regulator",
        "source_url": "https://nbebank.com/directives/",
        "confidence": "high",
        "related_indicator": None, "relationship_type": None,
        "impact_direction": None, "impact_magnitude": None,
        "impact_estimate": None, "lag_months": None, "evidence_basis": None,
        "comparable_country": None,
        "collected_by": COLLECTED_BY, "collection_date": COLLECTION_DATE,
        "original_text": (
            "NBE issued Directive FIS/01/2023 introducing a four-tier KYC framework, "
            "reducing onboarding requirements for basic mobile money accounts."
        ),
        "notes": "Parent event for impact_links ENC_0005–ENC_0012. Key regulatory trigger 2021-2024.",
    },
    # ── Impact Links ──────────────────────────────────────────────────────────
    # ENC_0005 — KYC Directive → ACCESS / ACC_OWNERSHIP
    {
        "record_id": "ENC_0005", "record_type": "impact_link", "category": None,
        "pillar": "ACCESS", "indicator": None, "indicator_code": None, "indicator_direction": None,
        "value_numeric": None, "value_text": None, "value_type": None, "unit": None,
        "observation_date": None, "period_start": None, "period_end": None,
        "fiscal_year": None, "gender": None, "location": None, "region": None,
        "source_name": "GSMA / World Bank FII", "source_type": "literature",
        "source_url": "https://www.gsma.com/mobilemoneymetrics/",
        "confidence": "medium",
        "related_indicator": "ACC_OWNERSHIP", "relationship_type": "enabling",
        "impact_direction": "increase", "impact_magnitude": "high",
        "impact_estimate": None, "lag_months": 12, "evidence_basis": "literature",
        "comparable_country": "Kenya",
        "collected_by": COLLECTED_BY, "collection_date": COLLECTION_DATE,
        "original_text": None,
        "notes": "KYC liberalisation linked to +8–12 pp account ownership in comparable SSA markets. parent_id=ENC_0004",
    },
    # ENC_0006 — KYC Directive → USAGE / USG_MM_VOLUME
    {
        "record_id": "ENC_0006", "record_type": "impact_link", "category": None,
        "pillar": "USAGE", "indicator": None, "indicator_code": None, "indicator_direction": None,
        "value_numeric": None, "value_text": None, "value_type": None, "unit": None,
        "observation_date": None, "period_start": None, "period_end": None,
        "fiscal_year": None, "gender": None, "location": None, "region": None,
        "source_name": "GSMA / NBE", "source_type": "literature",
        "source_url": "https://www.gsma.com/mobilemoneymetrics/",
        "confidence": "medium",
        "related_indicator": "USG_MM_VOLUME", "relationship_type": "enabling",
        "impact_direction": "increase", "impact_magnitude": "medium",
        "impact_estimate": None, "lag_months": 9, "evidence_basis": "literature",
        "comparable_country": "Ghana",
        "collected_by": COLLECTED_BY, "collection_date": COLLECTION_DATE,
        "original_text": None,
        "notes": "Lower friction onboarding raises P2P volume within 6-12 months of directive. parent_id=ENC_0004",
    },
    # ENC_0007 — KYC Directive → USAGE / USG_MM_ACTIVE_RATE
    {
        "record_id": "ENC_0007", "record_type": "impact_link", "category": None,
        "pillar": "USAGE", "indicator": None, "indicator_code": None, "indicator_direction": None,
        "value_numeric": None, "value_text": None, "value_type": None, "unit": None,
        "observation_date": None, "period_start": None, "period_end": None,
        "fiscal_year": None, "gender": None, "location": None, "region": None,
        "source_name": "GSMA", "source_type": "literature",
        "source_url": "https://www.gsma.com/mobilemoneymetrics/",
        "confidence": "medium",
        "related_indicator": "USG_MM_ACTIVE_RATE", "relationship_type": "enabling",
        "impact_direction": "increase", "impact_magnitude": "medium",
        "impact_estimate": None, "lag_months": 18, "evidence_basis": "literature",
        "comparable_country": "Tanzania",
        "collected_by": COLLECTED_BY, "collection_date": COLLECTION_DATE,
        "original_text": None,
        "notes": "KYC simplification linked to +5-8 pp active-use rate in comparable markets. parent_id=ENC_0004",
    },
    # ENC_0008 — KYC Directive → ACCESS / ACC_AGENT_COUNT
    {
        "record_id": "ENC_0008", "record_type": "impact_link", "category": None,
        "pillar": "ACCESS", "indicator": None, "indicator_code": None, "indicator_direction": None,
        "value_numeric": None, "value_text": None, "value_type": None, "unit": None,
        "observation_date": None, "period_start": None, "period_end": None,
        "fiscal_year": None, "gender": None, "location": None, "region": None,
        "source_name": "NBE / GSMA", "source_type": "literature",
        "source_url": "https://nbebank.com/payment-system-reports/",
        "confidence": "low",
        "related_indicator": "ACC_AGENT_COUNT", "relationship_type": "enabling",
        "impact_direction": "increase", "impact_magnitude": "low",
        "impact_estimate": None, "lag_months": 24, "evidence_basis": "literature",
        "comparable_country": None,
        "collected_by": COLLECTED_BY, "collection_date": COLLECTION_DATE,
        "original_text": None,
        "notes": "Tiered KYC lowers agent operational burden, incentivising network expansion. Low confidence (inferred). parent_id=ENC_0004",
    },
    # ENC_0009 — KYC Directive → AFFORDABILITY / AFF_COST_SEND
    {
        "record_id": "ENC_0009", "record_type": "impact_link", "category": None,
        "pillar": "AFFORDABILITY", "indicator": None, "indicator_code": None, "indicator_direction": None,
        "value_numeric": None, "value_text": None, "value_type": None, "unit": None,
        "observation_date": None, "period_start": None, "period_end": None,
        "fiscal_year": None, "gender": None, "location": None, "region": None,
        "source_name": "World Bank Remittance Prices", "source_type": "literature",
        "source_url": "https://remittanceprices.worldbank.org/",
        "confidence": "medium",
        "related_indicator": "AFF_COST_SEND", "relationship_type": "reducing_barrier",
        "impact_direction": "decrease", "impact_magnitude": "medium",
        "impact_estimate": None, "lag_months": 12, "evidence_basis": "literature",
        "comparable_country": "Uganda",
        "collected_by": COLLECTED_BY, "collection_date": COLLECTION_DATE,
        "original_text": None,
        "notes": "Increased digital account competition following KYC liberalisation lowers domestic transfer costs. parent_id=ENC_0004",
    },
    # ENC_0010 — Telebirr Expansion → USAGE / USG_MM_VOLUME
    {
        "record_id": "ENC_0010", "record_type": "impact_link", "category": None,
        "pillar": "USAGE", "indicator": None, "indicator_code": None, "indicator_direction": None,
        "value_numeric": None, "value_text": None, "value_type": None, "unit": None,
        "observation_date": None, "period_start": None, "period_end": None,
        "fiscal_year": None, "gender": None, "location": None, "region": None,
        "source_name": "Telebirr / Ethiopian Telecom", "source_type": "regulator",
        "source_url": "https://telebirr.com/",
        "confidence": "medium",
        "related_indicator": "USG_MM_VOLUME", "relationship_type": "enabling",
        "impact_direction": "increase", "impact_magnitude": "high",
        "impact_estimate": None, "lag_months": 6, "evidence_basis": "regulator",
        "comparable_country": None,
        "collected_by": COLLECTED_BY, "collection_date": COLLECTION_DATE,
        "original_text": None,
        "notes": "NBE directive enabled Telebirr expansion; 40M+ registered subscribers by Dec 2023. parent_id=ENC_0004",
    },
    # ENC_0011 — Fayda Digital ID → GENDER / GEN_ACCOUNT_OWN
    {
        "record_id": "ENC_0011", "record_type": "impact_link", "category": None,
        "pillar": "GENDER", "indicator": None, "indicator_code": None, "indicator_direction": None,
        "value_numeric": None, "value_text": None, "value_type": None, "unit": None,
        "observation_date": None, "period_start": None, "period_end": None,
        "fiscal_year": None, "gender": "female", "location": None, "region": None,
        "source_name": "ID4Africa / World Bank Fayda", "source_type": "literature",
        "source_url": "https://id4africa.com/2025/",
        "confidence": "medium",
        "related_indicator": "GEN_ACCOUNT_OWN", "relationship_type": "enabling",
        "impact_direction": "increase", "impact_magnitude": "medium",
        "impact_estimate": None, "lag_months": 18, "evidence_basis": "literature",
        "comparable_country": "Rwanda",
        "collected_by": COLLECTED_BY, "collection_date": COLLECTION_DATE,
        "original_text": None,
        "notes": "Fayda lowers ID barrier disproportionately benefiting women; expected to narrow gender gap. parent_id=EVT_0004",
    },
    # ENC_0012 — KYC Tiered Directive → GENDER / GEN_MM_SHARE
    {
        "record_id": "ENC_0012", "record_type": "impact_link", "category": None,
        "pillar": "GENDER", "indicator": None, "indicator_code": None, "indicator_direction": None,
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
        "notes": "Simplified KYC benefits women who lack formal proof of address. parent_id=ENC_0004",
    },
]

# ---------------------------------------------------------------------------
# 3. Merge and export
# ---------------------------------------------------------------------------

df_new = pd.DataFrame(enrichment_rows)

all_cols = list(df_raw.columns)
for col in df_new.columns:
    if col not in all_cols:
        all_cols.append(col)

df_new_aligned = df_new.reindex(columns=all_cols)
df_raw_aligned = df_raw.reindex(columns=all_cols)

df_enriched = pd.concat([df_raw_aligned, df_new_aligned], ignore_index=True)

csv_enriched = PROCESSED_DIR / "ethiopia_fi_enriched.csv"
df_enriched.to_csv(csv_enriched, index=False)
print(f"[✓] Wrote enriched CSV → {csv_enriched}  ({len(df_enriched)} records)")
print(f"    Base: {len(df_raw)} | Added: {len(df_new)} | Total: {len(df_enriched)}")
print(f"\nRecord type breakdown:")
print(df_enriched["record_type"].value_counts().to_string())

# ---------------------------------------------------------------------------
# 4. Validation — connect enrichment log to enriched CSV
# ---------------------------------------------------------------------------

print("\n" + "=" * 60)
print("ENRICHMENT LOG ↔ CSV SYNC VALIDATION")
print("=" * 60)

failures = []

# Check 1: Row count
expected_total = len(df_raw) + len(log_enc_ids)
actual_total = len(df_enriched)
check1_pass = actual_total == expected_total
status1 = "PASS" if check1_pass else "FAIL"
print(f"\n[{status1}] Check 1 — Row count")
print(f"       Base ({len(df_raw)}) + log ENC_ IDs ({len(log_enc_ids)}) = {expected_total}")
print(f"       Enriched CSV rows = {actual_total}")
if not check1_pass:
    failures.append(f"Row count mismatch: expected {expected_total}, got {actual_total}")

# Check 2: ID presence — every ENC_ in log must exist in CSV
csv_ids = set(df_enriched["record_id"].dropna().astype(str))
missing_ids = [enc_id for enc_id in log_enc_ids if enc_id not in csv_ids]
check2_pass = len(missing_ids) == 0
status2 = "PASS" if check2_pass else "FAIL"
print(f"\n[{status2}] Check 2 — ENC_ ID presence in CSV")
for enc_id in log_enc_ids:
    present = enc_id in csv_ids
    marker = "✓" if present else "✗"
    print(f"       {marker}  {enc_id}")
if not check2_pass:
    failures.append(f"IDs missing from CSV: {missing_ids}")

# Check 3: Required fields — non-null for all ENC_ rows in CSV
REQUIRED_FIELDS = ["source_url", "confidence", "collected_by", "collection_date"]
enc_rows = df_enriched[df_enriched["record_id"].astype(str).str.match(r"^ENC_\d{4}$")]
field_issues = {}
for field in REQUIRED_FIELDS:
    if field not in enc_rows.columns:
        field_issues[field] = "column absent"
        continue
    null_ids = enc_rows[enc_rows[field].isna()]["record_id"].tolist()
    if null_ids:
        field_issues[field] = null_ids

check3_pass = len(field_issues) == 0
status3 = "PASS" if check3_pass else "FAIL"
print(f"\n[{status3}] Check 3 — Required fields non-null for all ENC_ rows")
for field in REQUIRED_FIELDS:
    if field in field_issues:
        print(f"       ✗  {field:<22} — nulls in: {field_issues[field]}")
    else:
        print(f"       ✓  {field}")
if not check3_pass:
    failures.append(f"Required field nulls: {field_issues}")

# Final summary
print("\n" + "-" * 60)
if not failures:
    print("ALL CHECKS PASSED — enrichment log is in sync with enriched CSV.")
else:
    print(f"VALIDATION FAILED — {len(failures)} issue(s):")
    for f in failures:
        print(f"  • {f}")
    sys.exit(1)
print("=" * 60)
