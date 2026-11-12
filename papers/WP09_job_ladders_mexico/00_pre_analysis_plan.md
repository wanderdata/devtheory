# WP09 — Which jobs are rungs? Labour-market flows by sector, firm size and formality in Mexico

*Paul Wander. Pre-analysis plan, v0.1, 2026-11-12, written before any ENOE data were opened (D-046).*

Origin: RG01 paper 3, Donovan, Lu & Schoellman (2023, L136). Proposition P-RG3 (RG01 §3); related to P26 (WP08) and OQ-46.

## 1. Question

WP07 found that no sector's share of output reliably predicts growth. WP08 found that sector-level ladders hide dispersion within sectors (OQ-57). This study moves to the job.

A job is a *rung* if the person holding it tends to stay employed and to move to better-paid work, and a *dead end* if it churns back into non-employment or into equally poor work.

The question is which characteristics of a job predict rung behaviour in Mexico: its sector, or its firm size and formality.

**P-RG3.** Firm size and formality explain more of the variation across jobs in exit rates and upward transitions than sector does.
- **Supported if,** in the variance decomposition of §5.3, the size × formality cells account for a larger share of the between-cell variance of both outcomes than the sector cells, in both windows.
- **Rejected if** sector accounts for the larger share in both windows, or if, within size × formality cells, manufacturing jobs have significantly lower exit rates and higher upward-transition rates than service jobs. In that case the sector would be the more useful unit for this mechanism.
- **Inconclusive** if the result differs between windows or between the two outcomes.

## 2. Data

- **Survey.** Encuesta Nacional de Ocupación y Empleo (ENOE), INEGI, public microdata. It is a rotating panel of dwellings: each dwelling is interviewed in five consecutive quarters, and one fifth of the sample rotates out each quarter.
- **Two windows of five consecutive quarters each:**
  - **Pre-pandemic:** 2018 Q4 to 2019 Q4.
  - **Post-redesign:** 2023 Q1 to 2024 Q1. This uses ENOE^N, the edition in use since 2020 Q3, which includes telephone (CATI) interviews.

  Within a window, the rotation group that enters in its first quarter can be followed through all five visits. Shorter sequences come from the other groups. No window spans the 2020 break.
- **Tables:**
  - SDEMT (sociodemographic, with INEGI's precoded labour variables);
  - COE1T, for the tenure questions P3R_ANIO and P3R_MES (start date with the current employer);
  - HOGT, for the informant line, to flag proxy responses.
- **Sample:** ages 16–65, as in Donovan et al., with ages 15+ as a variant. Complete interviews only (R_DEF = 00) and usual or new residents (C_RES = 1 or 3). The main estimates cover the whole country; urban areas (CD_A, the 39 self-representing cities) are a variant, to match Donovan et al.'s urban benchmark.
- **Weights:** quarterly weight FAC_TRI (FAC in older files). For linked pairs, the origin-quarter weight is used, raked as in Donovan et al. (Appendix A.3) so that the linked sample matches the full origin sample by age group × sex × labour-force status.

## 3. Definitions

**States.** At each visit a person is in one of these:
- **N:** not employed. Unemployed and inactive are pooled, as in Donovan et al.'s benchmark, and kept separate in a variant.
- **E(s, k, f):** employed, in sector *s*, firm-size class *k* and formality status *f*.

| Dimension | Variable (SDEMT) | Classes used | To verify against the file description |
|---|---|---|---|
| Sector *s* | `rama_est2` | 11 groups; for comparison with WP08, also mapped to the 7 national-accounts sectors | mapping of codes |
| Firm size *k* | `ambito2` | own-account and micro without premises / micro with premises / small / medium / large / government / other or not specified | exact meaning of codes 1–8 |
| Formality *f* | `emp_ppal` | 1 informal, 2 formal (INEGI's labour informality definition: no access to social security through the job, or work in an informal unit) | — |
| Position | `pos_ocu` | employee / employer / own-account / unpaid | — |

The size classes and formality define 2 × 6 = 12 *size × formality cells*; sector defines 11 *sector cells*; together, at most 132 *job cells*. Cells with fewer than 200 unweighted origin observations in a window are merged with the nearest size class.

**Linking people across visits.** The person key is CD_A, ENT, CON, V_SEL, N_HOG, H_MUD and N_REN, with N_ENT rising by one between consecutive quarters. A match is accepted only if:
- sex is the same;
- age changes by −1 to +2 years between quarters;
- the match is unique.

Movers are lost because the survey follows dwellings. Match rates are reported by visit and by origin state, so selective attrition can be seen. Whether ENOE^N needs TIPO or another key in addition will be checked on the data: the key must be unique within a quarter.

## 4. Outcomes

Each outcome is defined for a person employed in cell *c* at visit *t*:

1. **Exit rate:** probability of being in N at *t*+1 (one quarter), and at *t*+4 (one year: first to fifth visit).
2. **Persistence:** probability of being in the same job cell at *t*+4.
3. **Upward transition:** probability of being, at *t*+4, employed in a cell whose median hourly earnings are higher than those of *c*. Cells are ranked by median hourly earnings of employees and own-account workers in the origin quarter, with fixed ranks within a window. Earnings are INEGI's `ing_x_hrs`. Its units will be checked against monthly income (`ingocup`) and weekly hours (`hrsocup`) before use (monthly income ÷ (4.3 × weekly hours)).
4. **Job change:** for employees, a different employer between *t* and *t*+1, identified by a start date with the current employer within the last three months (P3R_ANIO/P3R_MES), following Donovan et al.'s tenure-based definition (footnote 6). Whether these questions are asked in every quarter or only in the extended questionnaire will be checked; if only in the extended one, this outcome is computed for first-quarter visits only.
5. **Secondary: earnings growth** at *t*+4 for people employed at both dates, by origin cell. Income non-response is reported, and this outcome is not used to test P-RG3.

## 5. Analysis

### 5.1 Reproduce Donovan et al. for Mexico

Quarterly employment exit, job-finding and job-to-job rates for urban areas, ages 16–65, in 2018 Q4 to 2019 Q4. These are compared with the paper's Mexican figures, Mexico 1995–2017 in their Table 1. The comparison is only approximate, because the years differ. If the replication package becomes available, it is used for an exact comparison.

### 5.2 Rates by cell

Weighted rates for each outcome by sector cell, size × formality cell and job cell, in both windows, with 90% intervals. Intervals come from a bootstrap that resamples primary sampling units (UPM) within states, 499 replications.

### 5.3 Test of P-RG3: which dimension explains more

For each outcome *y* (exit at *t*+4; upward transition at *t*+4), on the person-level linked sample, with the origin-quarter weights:
- R² of *y* on sector dummies alone;
- R² of *y* on size × formality dummies alone;
- Shapley shares of the R² of *y* on both sets.

P-RG3 is supported if the size × formality share exceeds the sector share, with the bootstrap interval of the difference excluding zero, for both outcomes in both windows.

The second rejection condition is tested by a regression of *y* on manufacturing versus service-sector indicators, controlling for size × formality cells, age group, sex and education.

### 5.4 Measurement error

Misreported states create spurious transitions, which is the main threat here. Firm size and formality are reported with error, including by proxy respondents. Donovan et al. do not correct for this. The checks are:
- **(a) Confirmed transitions:** a move between *t* and *t*+1 counts only if the person is in the same state at *t*+2. Possible for people observed in three consecutive visits.
- **(b) No proxies:** the sample is limited to self-reported interviews (informant line equal to person line).
- **(c) Within-employer changes:** for employees whose start date with the employer is unchanged (same employer at both dates), the rate at which size or formality changes is reported. This measures misreporting directly, since the employer has not changed.

The test of P-RG3 is repeated under (a) and (b). If the conclusion changes, the main result is the version under (a).

### 5.5 What would change the conclusions

- **Selective attrition.** Linked people may differ from movers in ways related to the outcomes. A large difference in match rates between origin cells weakens the comparison between cells. Rates are reported with that difference.
- **Measurement error in (c).** If more than 10% of employees with the same employer change formality or size class from one quarter to the next, the size × formality transitions are dominated by misreporting. In that case outcome 3 is redefined on employer changes only.
- **Survey mode.** If the post-2020 window differs from the pre-2020 window mainly in telephone interviews, the difference between windows is not interpreted. Mode is controlled with TIPO.

## 6. What this does not do

- It describes which jobs are rungs. It does not estimate the effect of holding a job on later outcomes, because people are not assigned to jobs at random.
- It follows people for at most one year.
- It cannot estimate firm wage premia (no employer identifier).

## 7. Outputs

Only aggregate tables leave the raw-data folder. Code is in `empirics/code/enoe/`; tables go to `empirics/output/enoe/`; microdata stay in the uncommitted `empirics/data/raw/enoe/`.
