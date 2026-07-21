# Week 11 Final Submission — Forecasting Financial Inclusion in Ethiopia

**Trainee:** Abigiya Haile  
**Programme:** 10 Academy — KAIM 9  
**Week:** 11 — Data Exploration, Enrichment, and EDA  
**Submission date:** 2025-07-21  

---

## Rubric Coverage

### Task 1 — Data Exploration and Enrichment

| Criterion | Deliverable | Location |
|-----------|-------------|----------|
| Dataset loading (xlsx + reference codes) | `load_unified_data()`, `load_reference_codes()` | `src/data_loader.py` |
| Schema understanding | Schema constants, `validate_record()`, `print_schema_summary()` | `src/schema_utils.py` |
| Exploration by record_type | Bar chart + count table | `notebooks/01_data_exploration_enrichment.ipynb` §3.1 |
| Exploration by pillar | Colour-coded bar chart | §3.2 |
| Exploration by source_type & confidence | Side-by-side charts | §3.3 |
| Temporal range and indicator coverage | Date-range table + scatter plot | §3.4 |
| Data enrichment (12 new records) | 3 observations · 1 event · 8 impact_links | `data/processed/ethiopia_fi_enriched.csv` |
| Enrichment log — one row per record | Consolidated table with all 6 provenance fields | `data/data_enrichment_log.md` |
| Log ↔ CSV programmatic sync | `parse_log_enc_ids()` + 3 automated checks | `scripts/generate_enriched_csv.py` |
| Log ↔ CSV inline validation (notebook) | §4b — row-count · ID-presence · required-fields | `notebooks/01_data_exploration_enrichment.ipynb` §4b |
| Schema validation of enriched records | `validate_record()` called per ENC_ row | §4 |

### Task 2 — Exploratory Data Analysis

| Criterion | Deliverable | Location |
|-----------|-------------|----------|
| Dataset overview (shapes, dtypes, nulls) | Summary table + charts | `notebooks/02_eda_financial_inclusion.ipynb` §1 |
| Temporal coverage analysis | Year-by-year record count | §2 |
| Account ownership trajectory 2011–2024 | Line chart with growth-rate table | §3 |
| 2021–2024 slowdown investigation | Annotated zoom chart + narrative | §3 |
| Mobile money penetration | Registered vs active bar chart | §4 |
| P2P transaction volume trend | Area chart | §4 |
| Gender gap analysis | Side-by-side bar + gap annotation | §5 |
| Event timeline overlaid on indicator | Combined axis chart with 11 events | §6 |
| 6 key insights with evidence | Numbered insight blocks + citations | §7 |
| Data limitations assessment | 6 limitations + severity heatmap | §8 |

### Repository Best Practices

| Criterion | Deliverable |
|-----------|-------------|
| `.gitignore` | Python / Jupyter / data-science exclusions |
| `requirements.txt` | Pinned dependency groups |
| `README.md` | Project overview, schema docs, setup instructions, folder map |
| Logical folder structure | `src/` · `notebooks/` · `scripts/` · `data/raw/` · `data/processed/` · `references/` |
| Conventional commits | All commits follow `type(scope): description` format |

### Code Best Practices

| Criterion | Deliverable |
|-----------|-------------|
| Modular `src/` package | `data_loader.py` · `schema_utils.py` · `visualization.py` · `__init__.py` |
| Proper imports and error handling | Try/except on all file I/O; fallback paths |
| Reusable helper functions | `load_unified_data`, `get_observations`, `plot_account_ownership_trajectory`, etc. |
| Validation script with exit code | `scripts/generate_enriched_csv.py` exits 1 on failure |

---

## Repository Structure

```
Forecasting-Financial-Inclusion-in-Ethiopia/
├── data/
│   ├── raw/                          # Source xlsx files (read-only)
│   │   ├── ethiopia_fi_unified_data.xlsx
│   │   ├── reference_codes.xlsx
│   │   └── Additional Data Points Guide.xlsx
│   ├── processed/                    # Generated outputs
│   │   ├── ethiopia_fi_unified_data.csv   # 43 base records
│   │   └── ethiopia_fi_enriched.csv       # 55 records (base + ENC_0001–ENC_0012)
│   ├── data_enrichment_log.md        # Provenance log — one row per added record
│   └── README.md                     # Data dictionary
├── notebooks/
│   ├── 01_data_exploration_enrichment.ipynb  # Task 1
│   └── 02_eda_financial_inclusion.ipynb      # Task 2
├── references/                       # Source PDFs
├── scripts/
│   └── generate_enriched_csv.py      # Enrichment pipeline + log-CSV validation
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── schema_utils.py
│   └── visualization.py
├── .gitignore
├── README.md
├── SUBMISSION.md                     # This file
└── requirements.txt
```

---

## Enrichment Summary

| Record type | Base | Added | Total |
|-------------|------|-------|-------|
| observation | 30   | 3     | 33    |
| event       | 10   | 1     | 11    |
| target      | 3    | 0     | 3     |
| impact_link | 0    | 8     | 8     |
| **Total**   | **43** | **12** | **55** |

Enrichment records `ENC_0001`–`ENC_0012` are fully documented in
`data/data_enrichment_log.md` and validated against the enriched CSV by
`scripts/generate_enriched_csv.py` (all 3 sync checks pass).

---

## Key Findings (from Notebook 02)

1. **Account ownership grew from 22 % (2011) to 46 % (2024)** — a 24 pp gain over 13 years, but growth slowed sharply from 9 pp/year (2014–2021) to 3 pp (2021–2024).
2. **The 2021–2024 slowdown coincided with COVID-19 disruption** followed by the NBE Tiered KYC Directive (Mar 2023) which is expected to re-accelerate growth by 2025.
3. **Telebirr's 40 M+ subscribers mask a 30.5 % active-user rate** — registration far outpaced genuine usage, a key distinction for forecasting.
4. **750,000 licensed agents** provide infrastructure for rural outreach, but the registered-vs-active gap suggests supply-side expansion is ahead of demand-side adoption.
5. **The gender gap in account ownership is 14 pp** (male 53 %, female 39 % in 2024). The Fayda Digital ID programme is the most likely near-term lever to narrow this.
6. **Data sparsity is highest in AFFORDABILITY and QUALITY pillars** — both have fewer than 3 observations, limiting multi-pillar forecasting without additional enrichment.
