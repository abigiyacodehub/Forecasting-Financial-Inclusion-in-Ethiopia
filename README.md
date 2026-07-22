# Forecasting Financial Inclusion in Ethiopia

> Predicting the trajectory of financial inclusion in Ethiopia by combining sparse survey data with a rich catalogue of policy events, product launches, and regulatory changes — connected through a unified, schema-validated dataset.

---

## Project Overview

Ethiopia's financial inclusion story is one of rapid but uneven progress.  Account ownership grew from **22 % (2011) → 22 % (2014) → 35 % (2017) → 46 % (2021) → 49 % (2024)**, yet a 3-percentage-point gain over 2021–2024 sits alongside the explosive rise of Telebirr (launched May 2021) and the entry of Safaricom/M-Pesa (August 2023).  Understanding *why* growth slowed — and what will drive it next — requires linking quantitative indicators to their causal events.

This project builds that link using a **unified schema** that stores observations, events, targets, and causal impact_links in a single dataset, then applies forecasting techniques suited to limited, sparse time-series data.

---

## Repository Structure

```
.
├── data/
│   ├── raw/                          # Unmodified source files
│   │   ├── ethiopia_fi_unified_data.xlsx
│   │   ├── reference_codes.xlsx
│   │   └── Additional Data Points Guide.xlsx
│   ├── processed/                    # Cleaned & enriched outputs
│   │   ├── ethiopia_fi_unified_data.csv   # CSV export of raw data
│   │   └── ethiopia_fi_enriched.csv       # + new records from enrichment
│   ├── data_enrichment_log.md        # Audit trail for all additions
│   └── README.md                     # Detailed schema documentation
│
├── notebooks/
│   ├── 01_data_exploration_enrichment.ipynb   # Task 1 — load, explore, enrich
│   └── 02_eda_financial_inclusion.ipynb       # Task 2 — full EDA & insights
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py       # Load, filter, and join dataset functions
│   ├── schema_utils.py      # Validation, record constructors, schema docs
│   └── visualization.py     # Reusable Matplotlib chart functions
│
├── references/              # Background PDFs
│   ├── Global Findex Framework.pdf
│   ├── Forecasting Approaches for Limited Data.pdf
│   └── Building association matrices.pdf
│
├── Forecasting_Limited_Data.ipynb   # General forecasting tutorial (Week 11)
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Unified Data Schema

The dataset uses four **record types** stored in a single file.  The key design principle is: **do not pre-assign events to pillars**.

| record_type   | `pillar` column | `category` column | Description |
|---------------|-----------------|-------------------|-------------|
| `observation` | **Required**    | Empty             | Measured value from a primary source |
| `target`      | **Required**    | Empty             | Official policy goal |
| `event`       | **Empty**       | **Required**      | Policy / product / market event |
| `impact_link` | **Required**    | Empty             | Causal link from an event to a specific indicator |

### How impact_links work

```
EVT_0001  (event, product_launch) — Telebirr Launch
  └── IMP_0001  (impact_link, pillar=ACCESS,  related_indicator=ACC_OWNERSHIP)
  └── IMP_0002  (impact_link, pillar=USAGE,   related_indicator=USG_P2P_COUNT)
  └── IMP_0003  (impact_link, pillar=GENDER,  related_indicator=GEN_GAP_ACC)
```

One event → many impact_links, each carrying its own `pillar`, `relationship_type`, `impact_direction`, and `impact_magnitude`.

### Pillar definitions

| Pillar         | Measures |
|----------------|----------|
| `ACCESS`       | Can people reach services? (account ownership, 4G coverage, Fayda enrollment) |
| `USAGE`        | Are people actively using services? (P2P transactions, active accounts) |
| `AFFORDABILITY`| Can people afford services? (data cost as % of income) |
| `GENDER`       | Gender gaps across all dimensions |
| `QUALITY`      | Do services work reliably? |
| `TRUST`        | Do people trust the system? |
| `DEPTH`        | Beyond payments — savings, credit, insurance |

---

## Data Sources

| Source | Type | Indicators covered |
|--------|------|--------------------|
| World Bank Global Findex (2014, 2017, 2021, 2024) | `survey` | ACC_OWNERSHIP, ACC_MM_ACCOUNT, GEN_GAP_ACC |
| National Bank of Ethiopia (NBE) annual reports | `regulator` | Various |
| EthSwitch Annual Report | `operator` | USG_P2P_COUNT, USG_P2P_VALUE |
| Ethio Telecom LEAD Report | `operator` | ACC_4G_COV, Telebirr metrics |
| DataReportal Digital 2026 | `research` | ACC_MOBILE_PEN |
| GSMA Gender Gap Report | `research` | GEN_GAP_MOBILE |
| NFIS-II Strategy Document | `policy` | ACC_OWNERSHIP target |

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/abigiyacodehub/Forecasting-Financial-Inclusion-in-Ethiopia.git
cd Forecasting-Financial-Inclusion-in-Ethiopia
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate      # macOS / Linux
.venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Launch Jupyter

```bash
jupyter notebook
```

Then open `notebooks/01_data_exploration_enrichment.ipynb` to start.

---

## Notebooks

| Notebook | Purpose |
|----------|---------|
| `01_data_exploration_enrichment.ipynb` | Load the unified dataset, document the schema, explore all dimensions, and enrich with new records |
| `02_eda_financial_inclusion.ipynb` | Full EDA: temporal trends, access & usage analysis, event timeline, gender gaps, key insights |
| `Forecasting_Limited_Data.ipynb` | General tutorial on forecasting approaches for sparse data (reference material) |

---

## Key Findings (preview)

1. **Account ownership stalled (+3 pp, 2021–2024)** despite Telebirr reaching 40 M+ subscribers — suggesting a registration-vs-active-use gap.
2. **Mobile money account penetration doubled** (4.7 % → 9.5 %) in the same window, driven by Telebirr and M-Pesa entry.
3. **P2P transaction volume surged 158 %** in FY2024/25 vs FY2023/24, indicating usage deepening among existing users.
4. **Fayda digital ID** enrollment reached 15 M by May 2025 — a critical access enabler for the unbanked.
5. **Gender gap narrowed slightly** (20 pp → 18 pp), but female mobile money account share remains at only 14 %.

---

## Conventional Commit Style

This repository follows [Conventional Commits](https://www.conventionalcommits.org/):

```
feat(scope):     new feature or data
fix(scope):      bug fix
docs(scope):     documentation only
data(scope):     data enrichment or schema changes
refactor(scope): code restructuring
```

---

## License

MIT — see `LICENSE`.
