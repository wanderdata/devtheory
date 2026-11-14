# Doubling the Minimum Wage on Mexico's Northern Border: Earnings, Employment and Moves out of Informality, 2016–2019

*Paul Wander. Working draft v0.2, 2026-11-13. Pre-analysis plan: [`00_pre_analysis_plan.md`](00_pre_analysis_plan.md). Generated tables: [`empirics/output/enoe/border_mw/results.md`](../../../empirics/output/enoe/border_mw/results.md). App: Jobs in Mexico, page 9.4.*

## Abstract

In January 2019 Mexico doubled the minimum wage in the 43 municipalities of its northern border zone, raised it 16% elsewhere, and cut VAT and income tax in the same municipalities. We compare border-zone municipalities with the other municipalities of the six border states, using the national labour-force survey (ENOE) for 2016–2019 and only the sampling units in the survey before 2019. INEGI enlarged the sample in the border zone alone in 2019Q1, which would otherwise confound the comparison.

**Employment.** The package did not reduce employment. The employment rate of the population aged 15+ changed by +0.9 percentage points (90% interval −0.1 to +1.8).

**Reported earnings.** The distribution of reported earnings moved at the new minimum. The share of wage employees reporting less than it fell by 8.4 points, from a pre-period level of 47%, with fewer jobs below the minimum and more just above it, mostly in formal employment.

**Non-reporting.** At the same time, the share of wage employees reporting an amount of earnings fell by 7.8 points in the zone relative to the comparison group.
- About 1.6 points of this is a rise in answers to ENOE's follow-up question in ranges of the minimum wage. These answers are concentrated at "equal to the minimum".
- The rest is a rise in refusals and "don't know".

Allocating the range answers to earnings bins gives 5.6 fewer jobs below the minimum and 3.5 more just above it, per 100 people aged 15+. Even if every remaining new non-reporter earned less than the minimum, at least 2.6 jobs per 100 are missing from below it. Mean log earnings of those reporting an amount show no clear effect.

**Formality.** Moves from informal to formal work did not increase: −1.2 points a quarter (−5.0 to +1.6) against a pre-period rate of 18.5%. Neither the formal share of employment nor any other transition rate changed detectably.

## 1. Introduction

**The policy.** On 1 January 2019 the daily minimum wage in the Zona Libre de la Frontera Norte (ZLFN) rose from 88.36 to 176.72 pesos. In the rest of the country it rose to 102.68 pesos. The relative increase in the zone was 54 log points, among the largest minimum-wage changes studied anywhere. The same decree also, in the same municipalities and from the same date:
- reduced VAT from 16% to 8%;
- gave eligible firms an income-tax credit of one third, lowering the effective corporate rate from 30% to about 20%.

What any comparison of the zone with other places can identify is the effect of the package.

**Earlier work.**
- Using IMSS administrative records, Campos-Vázquez and Esquivel (2021) find higher formal earnings, concentrated at the bottom, and no effect on formal employment.
- Using ENOE, Alvarado Pérez, Orraca Romano and Cabrera-Hernandez (2023) find no effect on participation or employment, a rise of 1.4 points in the probability that a wage employee is formal, and hourly wage gains of about 3% among formal employees.
- Cabrera-Hernandez and Duval-Hernández (2026) use ENOE's first-quarter retrospective questions. They find fewer quits among formal workers, and new formal hires somewhat more likely to come from informal jobs.

**Contributions.** This paper adds four things:
1. It measures quarterly gross flows between formal work, informal work and non-employment in every quarter, by linking the same people across consecutive interviews. This addresses this programme's question of whether the policy moved people up the ladder of job types.
2. It measures where in the earnings distribution jobs appeared and disappeared, following Cengiz, Dube, Lindner and Zipperer (2019), separately for formal and informal wage employees.
3. It uses inference designed for about thirty treated clusters.
4. It documents two features of ENOE that bear on all ENOE-based studies of this policy:
   - the sample in the border zone was enlarged in 2019Q1, and only there;
   - earnings non-reporting rose in the zone after the increase.

## 2. Data

**Survey.** ENOE, the 17 quarters from 2016Q1 to 2020Q1. Persons aged 15+ with complete interviews are classified as formally employed, informally employed (INEGI's labour-informality definition) or not employed.

**Wage employees.** Aged 16–65. Their monthly labour income and hourly earnings are used when reported as positive.

**Treatment and comparison.**
- **Treatment.** Municipalities in the decree's list of 43, matched to INEGI's municipal codes. All municipalities that ENOE codes as belonging to the zone in 2019 are on the list. Thirty-one zone municipalities have observations in the main sample.
- **Comparison.** The other municipalities of the same six states: Baja California, Sonora, Chihuahua, Coahuila, Nuevo León and Tamaulipas.

**The 2019 sample expansion.** In 2019Q1 INEGI enlarged the ENOE sample in the border-zone municipalities:
- primary sampling units rose from 1,169 to 2,029, and records from about 20,800 to 34,000 a quarter;
- all five rotation groups grew in the same quarter;
- the comparison municipalities saw no change;
- survey weights were recalibrated, so the represented population barely changed.

A change in sample design at the date of the policy and only in the treated area could produce spurious differences, through new areas within municipalities or the different responses of first interviews. The main estimates therefore use only sampling units observed at least once in 2016–2018. Ordinary rotation removes these units at the same pace in both groups: 74% of the 2018 units in the zone and 72% elsewhere remain in 2020Q1.

**Linkage.** Persons are linked across consecutive quarters by dwelling, household and person identifiers, with checks on sex and age. Between 91.5% and 93.2% of those eligible are linked in every pair of quarters, with no break in 2019.

## 3. Method

**Cells.** Outcomes are weighted means or rates in municipality × quarter cells. Transition rates are computed in municipality × pair-of-quarters cells, for persons linked across the pair, by origin state.

**Difference in differences.** The model has municipality and quarter fixed effects and a single coefficient on zone × 2019. Cells are weighted by the municipality's average population aged 15+ in 2016–2018, which is fixed before treatment.

**Inference.** Standard errors are clustered by municipality. Because only about thirty clusters are treated, p-values and 90% intervals come from the restricted wild cluster bootstrap with Rademacher weights (Cameron, Gelbach and Miller 2008; MacKinnon and Webb 2018). Intervals are obtained by inverting the test.

**Event studies.** These replace the single coefficient with one per quarter, relative to 2018Q4. 2020Q1 is shown but excluded from averages: in 2020 the minimum wage rose 5% in the zone and 20% elsewhere, and fieldwork was interrupted in March.

**Earnings bins.** Wage employees are counted per person aged 15+ in bins of monthly earnings relative to the 2019 border minimum (5,302 pesos for 30 days), plus a bin for those not reporting an amount.
- **Missing jobs:** the sum of effects below the minimum.
- **Excess jobs:** the sum at 1.0–1.5 times the minimum.

**Decision rules.** Rules set in the plan treat an outcome as uninformative for the propositions if either holds:
- its pre-period coefficients are jointly different from zero (p < 0.10);
- for the earnings bins, if earnings reporting changes differentially by more than 3 points.

## 4. Results

### 4.1 Employment and formality

| Outcome | Estimate | 90% interval | Pre-period mean, zone |
|---|---|---|---|
| Employment rate, 15+ | +0.0087 | −0.0006 to +0.0178 | 0.610 |
| Formal employment rate, 15+ | +0.0069 | −0.0054 to +0.0198 | 0.381 |
| Formal share of employment | +0.0034 | −0.0195 to +0.0258 | 0.623 |
| Wage employees 16–65 per person 15+ | +0.0078 | −0.0010 to +0.0176 | 0.472 |
| Weekly hours, wage employees | +0.01 | −0.54 to +0.52 | 42.4 |

**No loss of employment.** The interval for the employment rate excludes any fall larger than 0.1 points. Across the robustness specifications the estimate ranges from −0.7 to +1.0 points, and none is significantly negative:
- the full sample;
- a national comparison group;
- comparison municipalities within 200 km of the zone;
- state × quarter effects;
- unweighted cells.

This agrees with the administrative evidence on formal employment and extends it to all employment.

**No change in formality.** There is no detectable change in formal employment or in the formal share. The point estimates are positive and small, and the intervals include changes of about ±2 points.

### 4.2 Transitions

Quarterly transition rates, difference in differences:

| Transition | Estimate | 90% interval | Pre-period rate, zone |
|---|---|---|---|
| Informal → formal | −0.0124 | −0.0503 to +0.0157 | 0.185 |
| Not employed → formal | +0.0008 | −0.0168 to +0.0121 | 0.067 |
| Formal → informal | −0.0020 | −0.0169 to +0.0103 | 0.104 |
| Formal → not employed | −0.0016 | −0.0144 to +0.0090 | 0.067 |
| Informal → not employed | +0.0029 | −0.0128 to +0.0217 | 0.191 |

**Moves out of informality.** These did not increase. The upper end of the interval for the informal-to-formal rate (+1.6 points) is below a tenth of the pre-period rate (1.85 points), which is the threshold set in the plan for rejecting P32. The rejection is narrow. The point estimate is negative in the main specification and in all robustness checks except unweighted cells.

**Other transitions.** Flows into and out of formal work did not change detectably either. The package did not move workers between rungs of the job ladder on a scale the survey can detect within a year.

### 4.3 Earnings

**The floor binds in the reported distribution.** The share of wage employees reporting earnings below the new minimum fell by 8.4 points (−12.0 to −5.4), from 47%.
- **Timing:** the event study shows a drop in 2019Q1 (−4.1 points) and −7 to −8 points in each later quarter of 2019.
- **Placebo:** a false treatment date of 2018Q1 gives −2.5 points (p = 0.45).
- **By schooling:** the effect is largest among workers with less than upper-secondary schooling (−11.3 points) and smaller among the rest (−4.8).

**Where the jobs moved.** Per 100 persons aged 15+:
- jobs below the minimum fell by 4.0 (formal 3.2, informal 0.8);
- jobs at 1.0–1.5 times the minimum rose by 2.4, all of them formal.

In formal employment the pattern is that of a binding floor: fewer formal jobs at 0.6–1.0 times the new minimum (−3.3) and more at 1.0–1.5 times (+2.5). In informal employment there are fewer jobs below the minimum and no more above it.

**Non-reporting rose at the same time.** The share of wage employees reporting any earnings fell by 7.8 points (−13.5 to −2.0) relative to the comparison group, from 77%. The decline appears from 2019Q2 and deepens through the year (event study: −7, −9 and −12 points in 2019Q2–Q4), with no pre-period movement (joint p = 0.72). Per 100 persons aged 15+, non-reporting wage employees rose by 3.9 (formal 2.7, informal 1.1).

The bins add up: the number of wage employees did not change significantly, and the fall below the minimum is matched by the rise just above it and among non-reporters. On amounts alone, two extremes bound the number of missing jobs:
- if every additional non-reporter would have reported less than the new minimum, the missing jobs are −0.2 per 100;
- if none would have, they are −4.0.

**Range answers.** Respondents who give no amount are asked whether their income is below, equal to, or in ranges of the minimum wage read out by the interviewer. That minimum is the one in force where they live: 5,302 pesos a month in the zone in 2019. A follow-up analysis set out in an addendum to the plan, before these answers were tabulated by zone or period, shows that range answers explain a small part of the fall in reporting.

| Answer, share of wage employees | Estimate | 90% interval | Pre-period mean, zone |
|---|---|---|---|
| Amount | −0.078 | −0.135 to −0.020 | 0.769 |
| Range (codes 1–7) | +0.016 | −0.010 to +0.041 | 0.083 |
| of which: below the minimum | +0.006 | +0.002 to +0.008 | 0.002 |
| of which: equal to the minimum | +0.012 | +0.005 to +0.021 | 0.005 |
| of which: 1–2 minimums | +0.018 | +0.004 to +0.037 | 0.033 |
| No answer (refused, don't know) | +0.063 | +0.016 to +0.104 | 0.148 |

- **Answers at the minimum.** "Equal to the minimum" rose from 0.5% of wage employees to about 1.7%, which is 79% of the net rise in range answers. This is what workers paid the new minimum would say. The higher ranges fell, partly because the yardstick read out had doubled.
- **The rest of the fall.** Most of the fall in reporting is a rise in refusals and "don't know" (+6.3 points), whose cause this survey cannot reveal. Plausible explanations include reluctance among workers paid less than the new legal minimum, and changes in fieldwork in the enlarged zone sample. Neither can be tested here.

**Corrected bins.** Each range answer is placed in the earnings bins by spreading it uniformly over its interval, with the minimum in force for that person and quarter, and a point for "equal to the minimum". Per 100 people aged 15+:
- **Missing jobs:** −5.6 below the minimum (−7.1 to −3.9).
- **Excess jobs:** +3.5 at 1.0–1.5 times it (+2.2 to +5.4); nearly all formal (+3.3).
- **Share below the minimum:** −11.8 points among those giving an amount or a range (−15.5 to −7.4). This measure passes the pre-trend test (p = 0.18).
- **Remaining non-response:** +3.0. If all of these people earned below the minimum, missing jobs would be −2.6. If none did, −5.6.

The shift of formal jobs from below to above the new minimum is therefore established in direction and bounded in size: between 2.6 and 5.6 jobs per 100 people aged 15+ moved out of the range below the minimum. The ratio of excess to missing jobs in the corrected bins is 0.63.

**Mean earnings.** Mean log hourly earnings of reporting wage employees rose by 1.5% (−1.8 to +6.3). The pre-period coefficients are jointly significant (p = 0.045), and the estimate depends on the comparison group: +4.7% with a national comparison group (p = 0.01), and +4.3% among workers with less schooling (p = 0.001). Own-account workers' hourly earnings rose by 2.9% (−3.9 to +9.2).

### 4.4 Propositions

- **P31** (higher low wages without less employment): **inconclusive** under the plan's rules (the addendum does not change the rule applied).
  - The employment part holds.
  - The earnings part cannot be judged under the plan's rules: log earnings and the below-minimum measures have pre-trends, and the bins are affected by the change in reporting.
  - The ratio of excess to missing jobs is 0.59.
- **P32** (more moves out of informality): **rejected**, narrowly.
- **P33** (a lighthouse effect on informal wages): **inconclusive**. Informal jobs below the minimum fell (−0.8 per 100, interval −1.6 to −0.1), but informal non-reporters rose by more (+1.1), and there are no excess informal jobs above the minimum.

### 4.5 Municipalities and distance to the zone's edge

**What the maps show.** The app maps each municipality with enough sample (16 zone and 42 comparison municipalities in 2019) before, during and after. The fall in the share earning below the minimum appears in most zone municipalities with enough sample:
- in 13 of the 16 shown, including Tijuana, Mexicali, Ensenada, Reynosa, Matamoros and Nogales, it falls by 5 to 19 points net of the comparison group;
- the exceptions are Nuevo Laredo (+1 point), Juárez (−2) and Tecate (−2).

**What the comparison municipalities show.** Their changes are centred on zero and vary no more than sampling error would produce. Empirical Bayes shrinkage pulls them almost entirely to their mean.

**Distance to the edge.** Plotted against the distance from the edge of the zone, the change is concentrated inside the zone. There is no gradient outside it within 200 km, which would appear if workers or firms near the edge responded to the zone's higher wages.

This is a picture of the difference in differences in space, not a separate estimate. Municipalities are large, few lie close to the edge, and distance is measured from municipal centroids.

## 5. Robustness and limits

- **The tax package.** Lower VAT and income tax in the zone could have offset part of the cost of the higher minimum, so employment effects of a minimum-wage increase alone could be less favourable.
- **Pre-trends.** The share earning below the minimum fell faster in the zone than elsewhere in 2016–2017, before stabilising from 2017Q4.
  - Starting the pre-period in 2017Q3, an analysis added after seeing the event studies, gives −7.1 points for the below-minimum share (−11.4 to −3.9), against −8.4 in the main specification.
  - The 2019 drop is far larger than any pre-period movement since 2017.
- **Non-reporting.** Range answers explain about a fifth of the fall in reporting, and are concentrated at the new minimum. The rest is refusals and "don't know", whose cause is not established. The corrected bins rely on spreading range answers uniformly within their intervals. For "below the minimum" and "equal to the minimum" this assumption does not affect which side of the minimum the answer falls on.
- **Survey design.** Restricting to pre-2019 sampling units avoids the 2019 sample expansion. The full sample gives almost identical estimates, for example −8.0 points for the below-minimum share and +0.8 for the employment rate.
- **Statistical power.** With about thirty treated municipalities and a quarterly panel of one year after the change, effects on transitions of a few points a quarter cannot be ruled out.

## 6. Conclusions

**Employment and the wage floor.** Doubling the minimum wage on Mexico's northern border, together with tax cuts, did not reduce employment. In formal employment it moved earnings from below the new floor to just above it, for between 2.6 and 5.6 jobs per 100 people aged 15+ once answers given in ranges of the minimum wage are counted. This is consistent with administrative evidence.

**Formality.** It did not move workers out of informality on a detectable scale. Informal-to-formal transitions, formal employment and the formal share were unchanged within a year. For the search for policies that move workers up the job ladder, a large minimum-wage increase in a region with a deep formal sector raised pay at the bottom of formal employment but did not by itself change who holds formal jobs.

**Measurement.** Two features of the survey matter for this and other ENOE-based evaluations of the policy:
- the expansion of the sample in the zone at the date of the policy;
- a fall in earnings reporting in the zone after it.

Counting answers given in ranges of the minimum wage recovers about a fifth of the lost reports and narrows the uncertainty about the wage effect. The rest, a rise in refusals, still limits what household-survey data can say about its exact size.

**What would change these conclusions:**
- evidence on why refusals rose in the zone, for example from interviewer or fieldwork records;
- a longer post-period that separates the 2019 change from the 2020 increases and the pandemic;
- administrative records that link formal hires to their previous informal status.

## Annex A. Notes on implementation and further work

**A.1 Design checks before estimation.** These used no outcome:
- counts of records and sampling units by quarter and group, which revealed the 2019 expansion;
- the match of the decree's list to INEGI codes;
- municipality codes, which are stored with leading spaces in some files and are converted to numbers.

Records with no municipality code (about 1% a quarter, outside self-represented cities) are excluded.

**A.2 Choices made after seeing results** (decision D-055):
- **Rule §6 made explicit in the report.** The rule was applied mechanically to the propositions: an outcome flagged by a pre-trend or by the change in reporting cannot support or reject a proposition.
- **Bounds on missing jobs** under extreme assumptions about non-reporters.
- **Addendum A1 to the plan** (D-056): range answers and corrected bins, written before tabulating the follow-up question by zone or period. H-A (most of the fall in reporting is range answers) is inconclusive; H-B (range answers concentrated at "equal to the minimum") is supported.
- **Byte-order marks.** Some 2016–2019 ENOE files begin with a UTF-8 byte-order mark; the reader now strips it. No earlier result used an affected column.
- **A pre-period starting in 2017Q3.**
- **Baja California Sur** added to the geometry, only to locate the zone's southern edge in Baja California.
- **Fit lines** in the distance plot drawn only over the observed range.

**A.3 Maps.** Municipal values are ratio estimates with variances from a bootstrap over primary sampling units within the municipality (200 replications). Changes are net of the population-weighted mean change among comparison municipalities, and are shrunk towards the mean of the municipality's group by a method-of-moments empirical Bayes estimator. Variances of changes ignore the positive covariance from repeated interviews of the same dwellings, so shrinkage is conservative.

**A.4 Further work.**
- **Refusals.** Examine who refuses (by formality, sex, schooling, establishment size) and whether refusals cluster by interviewer area in the enlarged zone sample.
- **IMSS records.** Link formal hires in the zone to their previous status, for a sharper test of moves out of informality.
- **Longer windows.** Extend to 2020Q3–2023 with ENOE^N, modelling the 2020–2023 increases in both regions (doses of 5–20% a year).
- **Prices.** Separate the tax cuts with price data.

## References

- Alvarado Pérez, R., Orraca Romano, P.P. and Cabrera-Hernandez, F. (2023). El efecto de duplicar el salario mínimo en la brecha de género en empleo y salarios en México. *El Trimestre Económico* 90(360): 961–999. [L151]
- Cabrera-Hernandez, F. and Duval-Hernández, R. (2026). Minimum wage and job transitions in Mexico. IZA Discussion Paper 18443. [L152]
- Cameron, A.C., Gelbach, J.B. and Miller, D.L. (2008). Bootstrap-based improvements for inference with clustered errors. *Review of Economics and Statistics* 90(3): 414–427. [L155]
- Campos-Vázquez, R.M. and Esquivel, G. (2021). The effect of doubling the minimum wage on employment and earnings in Mexico. *Economics Letters* 209: 110124. [L150]
- Cengiz, D., Dube, A., Lindner, A. and Zipperer, B. (2019). The effect of minimum wages on low-wage jobs. *Quarterly Journal of Economics* 134(3): 1405–1454. [L153]
- MacKinnon, J.G. and Webb, M.D. (2018). The wild bootstrap for few (treated) clusters. *Econometrics Journal* 21(2): 114–135. [L156]
- Decreto de estímulos fiscales región fronteriza norte, *Diario Oficial de la Federación*, 31 December 2018. [L154]
