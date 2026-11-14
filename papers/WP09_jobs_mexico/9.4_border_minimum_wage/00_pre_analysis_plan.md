# Study 9.4 — The 2019 border minimum wage: earnings, employment and moves out of informality

*Paul Wander. Pre-analysis plan v0.1, 2026-11-13. Written before any outcome was computed by treatment status or period. Design checks done before writing (sample sizes, municipality codes, sampling units) are reported in §2 and Annex A of the paper (D-054).*

## 1. Question and propositions

On 1 January 2019 the daily minimum wage in the 43 municipalities of the Zona Libre de la Frontera Norte (ZLFN) rose from 88.36 to 176.72 pesos. Elsewhere it rose 16%, to 102.68 pesos. The relative increase in the border zone was therefore about 54 log points. The same decree cut VAT from 16% to 8% and gave eligible firms an income-tax credit of one third, in the same municipalities and from the same date. What can be estimated is the effect of the package. It cannot be attributed to the minimum wage alone.

Earlier work finds:
- higher formal earnings and no detectable effect on formal employment, using IMSS records (Campos-Vázquez and Esquivel 2021);
- with ENOE, no effect on participation or employment and a small rise in formality among women (Alvarado Pérez, Orraca Romano and Cabrera-Hernandez 2023);
- fewer quits among formal workers, and new formal hires more likely to come from informal jobs, from the first-quarter retrospective questions (Cabrera-Hernandez and Duval-Hernández 2026).

This study adds four things:
- quarterly gross flows between formal work, informal work and non-employment, from the linked ENOE panel in every quarter;
- the change in the number of jobs at each level of earnings relative to the new minimum (Cengiz, Dube, Lindner and Zipperer 2019), separately for formal and informal wage employees;
- inference suited to about 26 treated municipalities;
- municipality-level maps and a plot of changes against distance to the edge of the zone.

The study also corrects for a change in the ENOE sample in the border zone in 2019 (§2).

**P31.** The package raised low wages in the border zone without reducing employment.
- **Supported if** all three hold:
  - mean log hourly earnings of wage employees rise (90% interval above zero);
  - the 90% interval for the employment rate of the population aged 15+ excludes a fall of 1.5 percentage points;
  - excess jobs at 1.0–1.5 times the new minimum are at least 0.7 times the missing jobs below it.
- **Rejected if** either holds:
  - the employment rate falls by at least 1 point with a 90% interval below zero;
  - the earnings effect is below 2% and its interval includes zero.
- **Inconclusive** otherwise.

**P32.** The package increased moves out of informality: the quarterly rate at which informal workers become formal rose in the border zone.
- **Supported if** both hold:
  - the effect on the informal-to-formal transition rate is positive with a 90% interval above zero;
  - the formal employment rate does not fall (90% interval not entirely below zero).
- **Rejected if** the 90% interval excludes an increase of 10% of the pre-period mean rate in the border zone.
- **Inconclusive** otherwise.

**P33.** The new minimum also moved the earnings of informal wage employees, the "lighthouse" effect: informal jobs paying less than the new minimum fell.
- **Supported if** the sum of effects on informal wage employees in bins below the new minimum is negative with a 90% interval below zero.
- **Rejected if** the 90% interval excludes a fall of a quarter of the pre-period mass of informal wage employees below the new minimum in the border zone.
- **Inconclusive** otherwise.

## 2. Data, samples and the 2019 sample expansion

- **Survey.** ENOE, every quarter from 2016Q1 to 2020Q1 (17 quarters). 2020Q2 has no ENOE. 2020Q1 is shown in event studies but excluded from the post-period average, for two reasons:
  - in 2020 the minimum wage rose 20% outside the zone and 5% inside it, narrowing the difference;
  - fieldwork was interrupted by the pandemic in March 2020.
- **Treatment.** Municipalities (`ent`, `mun`) in the decree's list of 43, matched to INEGI codes. All 29 municipalities that ENOE codes `zona` = 1 in 2019 are on the list. Records with no municipality code (about 1%, outside self-represented cities) are excluded.
- **Control.** Main: the other municipalities of the six border states (Baja California, Sonora, Chihuahua, Coahuila, Nuevo León, Tamaulipas). Robustness:
  - all other municipalities in Mexico;
  - control municipalities within 200 km of the zone's edge.
- **Sample expansion.** In 2019Q1 INEGI enlarged the sample in the border zone:
  - primary sampling units in the treated municipalities rose from 1,169 to 2,029, and records from about 20,800 to 34,000 a quarter;
  - all five rotation groups grew at once;
  - nothing changed in the control municipalities;
  - weighted totals were recalibrated, so the represented population barely changed.

  A sample change at the treatment date and only in treated areas could bias any before–after comparison. The **main specification uses only sampling units observed at least once in 2016Q1–2018Q4.** These units rotate out at the same pace in treated and control areas: 74% and 72% of the 2018 units remain in 2020Q1. **Robustness:** the full sample. As a diagnostic, the paper compares old and new units within the border zone in 2019.
- **Samples by outcome.**
  - Population aged 15+ for employment rates and flows.
  - Wage employees aged 16–65 (`pos_ocu` = 1) for earnings. Monthly labour income is `ingocup` and hourly earnings `ing_x_hrs`, both among those reporting positive income. Non-reporting is analysed as an outcome.
- **Formality.** INEGI's labour-informality definition (`emp_ppal`).

## 3. Estimation

**Cells.** Weighted means and rates by municipality × quarter (survey weight `fac`). For flows, the cell is the municipality × consecutive pair of quarters, among persons linked across the pair (the study 9.1 linkage: `enoe_link.link`).

**Difference in differences.** For outcome *y* in municipality *m* and quarter *t*:

  y_mt = α_m + δ_t + β · ZLFN_m · Post_t + ε_mt

- Post is 2019Q1–2019Q4; 2020Q1 is dropped.
- Cells are weighted by the municipality's average weighted population aged 15+ over 2016–2018, so that weights do not respond to treatment.

**Event study.** The same model with one coefficient per quarter, relative to 2018Q4. Pre-trends are tested jointly on the eleven pre-period coefficients.

**Inference.**
- Standard errors clustered by municipality (CR1).
- With about 26 treated clusters, p-values and 90% intervals come from the wild cluster bootstrap: restricted for p-values, Rademacher weights, 1,999 replications; intervals by inverting the restricted test on a grid.
- The judgements in §1 use the bootstrap intervals.

**Earnings bins** (Cengiz et al. 2019). Monthly labour income of wage employees relative to M = 5,302 pesos, the 2019 border minimum for 30 days. Bins:
- [0, 0.6), [0.6, 0.8), [0.8, 1.0), [1.0, 1.2), [1.2, 1.5), [1.5, 2), [2, 3), ≥ 3;
- employed with income not reported.

For each bin and formality status, the outcome is wage employees in the bin per person aged 15+. The model is run bin by bin with the same fixed effects. Bins are fixed in nominal pesos; quarter effects absorb common inflation.
- **Missing jobs:** the sum of effects below 1.0.
- **Excess jobs:** the sum over [1.0, 1.5).
- Both are reported relative to the border zone's pre-period mass below M.

**Transitions.** Quarterly rates by origin, among persons aged 15+ linked across consecutive quarters, assigned to the municipality of the origin quarter:
- informal → formal (P32);
- not employed → formal;
- formal → informal;
- formal → not employed;
- informal → not employed.

**Heterogeneity** (secondary): women and men; schooling below and above upper secondary.

## 4. Maps and the discontinuity plot

ENOE is not designed to be representative at municipality level, so the maps are descriptive and built to avoid overstating precision:
- **Units.** Only municipalities with at least 300 weighted-sample records in each period are coloured. Others are shown in grey; municipalities outside the six states are not drawn.
- **Periods.** Before (2016Q1–2018Q4), during (2019Q1–2019Q4) and after (2020Q1).
- **Values.** For each outcome:
  - the level before;
  - the change from before to each later period, net of the mean change among control municipalities.
- **Shrinkage.** Changes are shrunk towards the mean of the municipality's group (zone or control) by empirical Bayes. Sampling variances come from a bootstrap over primary sampling units within the municipality, so changes measured on small samples move towards the group mean.
- **Boundaries.** CONABIO/INEGI 2020 municipal boundaries (public GeoJSON derived from INEGI's Marco Geoestadístico), simplified for display. San Quintín (created in 2020 from Ensenada) is merged back into Ensenada.
- **Mapped outcomes:**
  - share of wage employees earning below M;
  - mean log hourly earnings;
  - formal share of employment;
  - informal-to-formal transition rate.
- **Discontinuity plot.** Each municipality's net change (2019 against before) is plotted against the signed distance from its centroid to the edge of the zone, negative inside and positive outside, with sample-weighted local linear fits on each side.
  - It is a picture of the difference in differences across space, not a separate estimate. Municipalities are large and few lie close to the edge.
  - Distance is measured from geometric centroids, which can lie far from where people live in large municipalities such as Ensenada or Caborca.

## 5. Robustness

- Full sample, including the 2019 expansion.
- National control group; control municipalities within 200 km.
- State × quarter effects. Baja California has no control municipality and drops out.
- Unweighted cells; individual-level regression with the same fixed effects for the main outcomes.
- Hourly instead of monthly earnings for the bins.
- Placebo: the same design with a false treatment date of 2018Q1, on 2016Q1–2018Q4.

## 6. What would change the conclusions

- **Differential trends.** Pre-trends in the event study (a joint test with p < 0.10 for a primary outcome) make that outcome's estimate unreliable; this is reported as such.
- **Differential non-reporting.** A change in earnings non-reporting in the zone of more than 3 percentage points relative to controls would make the earnings bins unreliable.
- **Confounding by the tax package.** VAT and income-tax cuts would bias employment effects upward relative to a pure minimum-wage effect. Nothing in ENOE separates the two.
