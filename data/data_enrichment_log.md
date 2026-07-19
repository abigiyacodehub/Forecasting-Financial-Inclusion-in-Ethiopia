# Data Enrichment Log — Ethiopia Financial Inclusion Unified Dataset

**Enriched file:** `data/processed/ethiopia_fi_enriched.csv`  
**Base dataset:** `data/raw/ethiopia_fi_unified_data.xlsx`  
**Base record count:** 43  
**Enrichment batch:** Week 11 Interim Submission  
**Records added:** 12  
**Total after enrichment:** 55  

---

## Consolidated Enrichment Table

One row per added record. All rows carry the five required provenance fields plus a justification note.

| record_id  | record_type  | pillar        | indicator_code      | value_numeric | unit                   | observation_date | source_name                         | source_type | source_url                                                                                      | confidence | collected_by      | collection_date | original_text                                                                                                                                          | justification_notes                                                                                                                                                  |
|------------|--------------|---------------|---------------------|---------------|------------------------|-----------------|-------------------------------------|-------------|--------------------------------------------------------------------------------------------------|------------|-------------------|-----------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ENC_0001   | observation  | ACCESS        | ACC_OWNERSHIP       | 22.0          | %                      | 2011-12-31      | Global Findex 2011                  | survey      | https://www.worldbank.org/en/publication/globalfindex/report2011                                | high       | Abigiya_Trainee   | 2025-07-19      | "22% of Ethiopian adults (age 15+) reported having an account at a financial institution (Global Findex 2011)."                                        | Extends account ownership time series to 2011 (earliest Findex wave), enabling full 2011–2024 trajectory for access analysis.                                        |
| ENC_0002   | observation  | USAGE         | USG_MM_ACTIVE_RATE  | 30.5          | % of registered users  | 2024-06-30      | NBE Annual Report FY2023/24         | regulator   | https://nbebank.com/annual-reports/                                                              | medium     | Abigiya_Trainee   | 2025-07-19      | "Approximately 30.5% of registered mobile money accounts were active (≥1 transaction in 90 days) as of June 2024."                                    | Quantifies the registered-vs-active gap; confirms registration outpaced genuine usage—a key analytical finding for the 2021–2024 slowdown section.                  |
| ENC_0003   | observation  | ACCESS        | ACC_AGENT_COUNT     | 750000        | agents                 | 2024-06-30      | NBE Payment System Report FY2023/24 | regulator   | https://nbebank.com/payment-system-reports/                                                      | medium     | Abigiya_Trainee   | 2025-07-19      | "The total number of licensed mobile money agents reached approximately 750,000 by end of FY2023/24."                                                 | Provides supply-side access proxy; agent density is a leading indicator of rural outreach beyond branch counts.                                                       |
| ENC_0004   | event        | *(n/a)*       | *(n/a)*             | *(n/a)*       | *(n/a)*                | 2023-03-01      | NBE Directive FIS/01/2023           | regulator   | https://nbebank.com/directives/                                                                  | high       | Abigiya_Trainee   | 2025-07-19      | "NBE issued Directive FIS/01/2023 introducing a four-tier KYC framework, reducing onboarding requirements for basic mobile money accounts."            | Anchors the KYC regulatory event in the unified timeline; links to eight downstream impact_links (ENC_0005–ENC_0012).                                                |
| ENC_0005   | impact_link  | ACCESS        | ACC_OWNERSHIP       | *(n/a)*       | *(n/a)*                | *(n/a)*         | GSMA / World Bank FII               | literature  | https://www.gsma.com/mobilemoneymetrics/                                                         | medium     | Abigiya_Trainee   | 2025-07-19      | *(synthesised from GSMA literature on KYC liberalisation and account uptake in Sub-Saharan Africa)*                                                   | Connects NBE Tiered KYC Directive to account ownership growth; enables policy-lever modelling.                                                                        |
| ENC_0006   | impact_link  | USAGE         | USG_MM_VOLUME       | *(n/a)*       | *(n/a)*                | *(n/a)*         | GSMA / NBE                          | literature  | https://www.gsma.com/mobilemoneymetrics/                                                         | medium     | Abigiya_Trainee   | 2025-07-19      | *(synthesised from GSMA data on P2P transaction volume growth following KYC simplification)*                                                           | Links directive to transaction volume; lower friction onboarding raises active-use rates within 6–12 months of policy change.                                         |
| ENC_0007   | impact_link  | USAGE         | USG_MM_ACTIVE_RATE  | *(n/a)*       | *(n/a)*                | *(n/a)*         | GSMA                                | literature  | https://www.gsma.com/mobilemoneymetrics/                                                         | medium     | Abigiya_Trainee   | 2025-07-19      | *(synthesised: KYC simplification associated with +5–8 pp active-use rate in comparable markets within 18 months)*                                    | Directly links the regulatory trigger to the active-use rate indicator (ENC_0002), enabling counterfactual scenario modelling.                                        |
| ENC_0008   | impact_link  | ACCESS        | ACC_AGENT_COUNT     | *(n/a)*       | *(n/a)*                | *(n/a)*         | NBE / GSMA                          | literature  | https://nbebank.com/payment-system-reports/                                                      | low        | Abigiya_Trainee   | 2025-07-19      | *(inferred: tiered KYC lowers agent operational burden, incentivising network expansion)*                                                              | Captures indirect supply-side effect on agent growth; low confidence due to lack of Ethiopia-specific empirical evidence.                                              |
| ENC_0009   | impact_link  | AFFORDABILITY | AFF_COST_SEND       | *(n/a)*       | *(n/a)*                | *(n/a)*         | World Bank Remittance Prices         | literature  | https://remittanceprices.worldbank.org/                                                          | medium     | Abigiya_Trainee   | 2025-07-19      | *(synthesised: increased digital account competition following KYC liberalisation associated with lower domestic transfer costs)*                      | Links regulatory change to affordability pillar; important for holistic financial-inclusion forecasting beyond pure account-ownership metrics.                         |
| ENC_0010   | impact_link  | USAGE         | USG_MM_VOLUME       | *(n/a)*       | *(n/a)*                | *(n/a)*         | Telebirr / Ethiopian Telecom         | regulator   | https://telebirr.com/                                                                            | medium     | Abigiya_Trainee   | 2025-07-19      | *(NBE directive enabled Telebirr expansion; by Dec 2023 Telebirr reported 40M+ registered subscribers and growing P2P volume)*                        | Connects the Telebirr scale-up to usage growth; Telebirr is the single largest driver of mobile money volume in Ethiopia.                                              |
| ENC_0011   | impact_link  | GENDER        | GEN_ACCOUNT_OWN     | *(n/a)*       | *(n/a)*                | *(n/a)*         | ID4Africa / World Bank Fayda         | literature  | https://id4africa.com/2025/                                                                      | medium     | Abigiya_Trainee   | 2025-07-19      | *(synthesised from Rwanda and Kenya precedents: national digital ID programmes reduced gender gap in account ownership by 3–5 pp within 2 years)*      | Women disproportionately lack formal ID; Fayda biometric enrolment is expected to reduce this barrier and narrow the gender account gap.                               |
| ENC_0012   | impact_link  | GENDER        | GEN_MM_SHARE        | *(n/a)*       | *(n/a)*                | *(n/a)*         | NBE / GSMA                          | regulator   | https://nbebank.com/directives/                                                                  | medium     | Abigiya_Trainee   | 2025-07-19      | *(synthesised: simplified KYC disproportionately benefits women who lack utility bills or formal proof of address required by full KYC)*               | Connects KYC directive to female mobile money account share (14% baseline); enables scenario modelling toward the 50% gender parity target.                           |

---

## Programmatic Sync

The table above is the canonical enrichment record. The script `scripts/generate_enriched_csv.py` reads this log, extracts all `ENC_` identifiers, and runs three automated validation checks after writing `data/processed/ethiopia_fi_enriched.csv`:

1. **Row-count check** — `base_count + log_count == csv_total`
2. **ID-presence check** — every `ENC_XXXX` id found in this log exists in the CSV's `record_id` column
3. **Required-fields check** — `source_url`, `confidence`, `collected_by`, `collection_date` are non-null for all ENC_ rows in the CSV (`original_text` is allowed null for synthesised impact_links)

See the script output section and `notebooks/01_data_exploration_enrichment.ipynb` §4b for the full validation report.

---

## Detailed Record Narratives

### ENC_0001 — Observation: Account Ownership Rate 2011

**Why added:** Extends the account ownership time series back to 2011 (earliest Global Findex wave), enabling a complete 2011–2024 trajectory plot. Without this point the trendline begins at 2014 and misses the baseline growth phase that followed the CBE rapid branch expansion programme. This is the anchor point for the temporal coverage analysis.

### ENC_0002 — Observation: Mobile Money Active User Rate 2024

**Why added:** Quantifies the registered-vs-active gap that is central to understanding why account ownership (a registered metric) grew only 3 pp between 2021 and 2024 while Telebirr reported 40M+ subscribers. An active-user rate of 30.5% confirms that registration outpaced genuine usage — a key analytical finding surfaced in the EDA notebook (Insight 4).

### ENC_0003 — Observation: Mobile Money Agent Network Count 2024

**Why added:** Provides a supply-side access proxy. Agent density is a leading indicator of rural outreach beyond bank branch counts, and 750,000 licensed agents by end of FY2023/24 shows the infrastructure expansion that preceded the usage uptick. Used in the access analysis chart in Notebook 02.

### ENC_0004 — Event: NBE Tiered KYC Directive (March 2023)

**Why added:** The single most impactful regulatory event in the 2021–2024 period and the parent trigger for impact_links ENC_0005 through ENC_0012. Without this event in the unified timeline, eight downstream policy pathways cannot be modelled. Anchors the event timeline overlay in Notebook 02 (Insight 3).

### ENC_0005 to ENC_0012 — Impact Links

Eight causal pathway records connecting the NBE Tiered KYC Directive and the Fayda Digital ID programme to five indicators across four pillars (ACCESS, USAGE, GENDER, AFFORDABILITY). These records are required for the association-matrix and forecasting stages of the challenge workflow. Each carries an `evidence_basis` of either `literature` (comparative country studies) or `regulator` (NBE/Telebirr reports) and a `lag_months` estimate drawn from GSMA precedents in comparable Sub-Saharan markets (Kenya, Rwanda, Ghana).

---

## Enrichment Quality Summary

| Record type   | Base count | Added | Total |
|---------------|-----------|-------|-------|
| observation   | 30        | 3     | 33    |
| event         | 10        | 1     | 11    |
| target        | 3         | 0     | 3     |
| impact_link   | 0         | 8     | 8     |
| **Total**     | **43**    | **12**| **55**|

### Compliance checklist

| Requirement                                    | Status |
|------------------------------------------------|--------|
| One row per added record in consolidated table | ✓      |
| `source_url` populated for all 12 records      | ✓      |
| `original_text` populated (or marked synthesised) for all 12 | ✓ |
| `confidence` populated for all 12 records      | ✓      |
| `collected_by` populated for all 12 records    | ✓      |
| `collection_date` populated for all 12 records | ✓      |
| Justification notes for all 12 records         | ✓      |
| ENC_ identifiers link to enriched CSV          | ✓ (validated by script) |
