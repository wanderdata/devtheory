# The 2019 Minimum-Wage Increase in Mexico's Northern Border Zone: Employment, Earnings and Transitions out of Informality

*Paul Wander. Working draft v0.3, 2026-11-16. Pre-analysis plan and addendum: [`00_pre_analysis_plan.md`](00_pre_analysis_plan.md). Generated tables: [`empirics/output/enoe/border_mw/results.md`](../../../empirics/output/enoe/border_mw/results.md). App: Jobs in Mexico, page 9.4.*

## Abstract

In January 2019 the daily minimum wage in the 43 municipalities of Mexico's northern border zone rose from 88.36 to 176.72 pesos, against an increase of 16% elsewhere; VAT and income tax were cut in the same municipalities from the same date. Using the national labour-force survey (ENOE) for 2016Q1–2019Q4, this paper compares zone municipalities with the other municipalities of the six border states in a difference-in-differences design, restricted to sampling units observed before 2019 because INEGI enlarged the sample in the zone, and only there, in 2019Q1. Inference uses the restricted wild cluster bootstrap with 31 treated municipalities. The employment rate of the population aged 15 and over changed by 0.9 percentage points (90% interval −0.1 to 1.8), and the quarterly rate of transition from informal to formal employment by −1.2 points (−5.0 to 1.6) on a base of 18.5%. The share of wage employees reporting monthly earnings below the new minimum fell by 8.4 points (−12.0 to −5.4) from 47%, while the share reporting any amount fell by 7.8 points (−13.5 to −2.0). Counting answers given in ranges of the minimum wage, the share below the minimum fell by 11.8 points (−15.5 to −7.4). Estimates of the number of jobs that moved from below to above the minimum fail the plan's pre-trend test and are reported as descriptive.

## 1. Introduction

On 1 January 2019 the daily minimum wage in the Zona Libre de la Frontera Norte rose from 88.36 to 176.72 pesos, while in the rest of the country it rose to 102.68 pesos, so that the relative increase in the zone was 54 log points. The same decree reduced VAT from 16% to 8% in the zone and gave eligible firms an income-tax credit of one third, lowering the effective corporate rate from 30% to about 20%. A comparison of the zone with other places identifies the effect of this package, not of the minimum wage alone.

Using IMSS administrative records, Campos-Vázquez and Esquivel (2021) find higher formal earnings, concentrated at the bottom of the distribution, and no effect on formal employment. Using ENOE, Alvarado Pérez, Orraca Romano and Cabrera-Hernandez (2023) find no effect on participation or employment, an increase of 1.4 points in the probability that a wage employee is formal, and hourly wage gains of about 3% among formal employees. Using the retrospective questions that ENOE asks in first quarters, Cabrera-Hernandez and Duval-Hernández (2026) find fewer quits among formal workers and a somewhat higher share of new formal hires coming from informal jobs.

This paper adds quarterly gross flows between formal employment, informal employment and non-employment, measured by linking the same persons across consecutive interviews in every quarter; estimates of employment by earnings bin relative to the new minimum, following Cengiz, Dube, Lindner and Zipperer (2019), separately for formal and informal wage employees; and inference suited to about thirty treated clusters. It also documents two features of ENOE that affect any survey-based evaluation of the policy: the 2019 expansion of the sample in the zone and a fall in earnings reporting there after the increase.

## 2. Data

The paper uses the 17 ENOE quarters from 2016Q1 to 2020Q1. Persons aged 15 and over with complete interviews are classified as formally employed, informally employed (INEGI's labour-informality definition) or not employed. Wage employees are those aged 16–65 in subordinate paid employment; their monthly labour income and hourly earnings are used when reported as positive.

The treatment group consists of the municipalities in the list of 43, matched to INEGI's municipal codes. Thirty-four of them appear in the sample at some point. The 29 sampled in 2019 are all coded as belonging to the zone by ENOE's own zone variable; the other five (Guerrero and Ocampo in Coahuila, Naco and Sáric in Sonora, Miguel Alemán in Tamaulipas) appear only before 2019 and contribute no observations after the change. Thirty-one zone municipalities have cells in the main sample. The comparison group consists of the other municipalities of Baja California, Sonora, Chihuahua, Coahuila, Nuevo León and Tamaulipas.

In 2019Q1 INEGI enlarged the ENOE sample in the zone municipalities. Primary sampling units rose from 1,169 to 2,029 and records from about 20,800 to 34,000 a quarter, in all five rotation groups at once; the comparison municipalities were unaffected, and survey weights were recalibrated so that the represented population barely changed. Because a change in sample design at the date of the policy and only in the treated area could produce spurious differences, the main estimates use only sampling units observed at least once in 2016–2018. Ordinary rotation removes these units at the same pace in both groups: 74% of the units observed in 2018 in the zone, and 72% elsewhere, remain in 2020Q1. In 2019 the added units resemble the existing ones: the employment rate is 62.6% in the added units and 61.0% in the existing ones, the formal share 63.9% and 62.7%, the share of wage employees reporting earnings 75.8% and 74.5%, and the share reporting less than the new minimum 30.3% and 29.1%.

Persons are linked across consecutive quarters by dwelling, household and person identifiers, with checks on sex and age; between 91.5% and 93.2% of eligible persons are linked in every pair of quarters, with no break in 2019.

## 3. Estimation

Outcomes are weighted means or rates in municipality × quarter cells; transition rates are computed in municipality × pair-of-quarters cells for persons linked across the pair. The difference-in-differences model has municipality and quarter fixed effects and a single coefficient on zone × 2019, with cells weighted by the municipality's average population aged 15 and over in 2016–2018. Standard errors are clustered by municipality. Because about thirty clusters are treated, p-values come from the restricted wild cluster bootstrap with Rademacher weights and 1,999 replications, and 90% intervals from inverting the bootstrap test on a grid with 999 replications (Cameron, Gelbach and Miller 2008; MacKinnon and Webb 2018). Event studies replace the single coefficient with one per quarter relative to 2018Q4. 2020Q1 is shown but not used in averages, because in 2020 the minimum wage rose 5% in the zone and 20% elsewhere and fieldwork was interrupted in March.

Wage employees are counted per person aged 15 and over in bins of monthly earnings relative to the 2019 zone minimum (5,302 pesos for 30 days), with a separate bin for those not reporting an amount. Missing jobs are the sum of effects below the minimum and excess jobs the sum at 1.0–1.5 times the minimum.

The plan's §6 treats an outcome as uninformative for the propositions if its pre-period event-study coefficients are jointly different from zero (p < 0.10), and treats the earnings bins as unreliable if earnings reporting changes differentially by more than 3 points.

## 4. Results

### 4.1 Employment and formality

*Table 1. Difference-in-differences estimates: employment and formality*

| Outcome | Estimate | 90% interval | Pre-period mean, zone |
|---|---|---|---|
| Employment rate, 15+ | 0.0087 | −0.0006 to 0.0178 | 0.610 |
| Formal employment rate, 15+ | 0.0069 | −0.0054 to 0.0198 | 0.381 |
| Formal share of employment | 0.0034 | −0.0195 to 0.0258 | 0.623 |
| Wage employees 16–65 per person 15+ | 0.0078 | −0.0010 to 0.0176 | 0.472 |
| Weekly hours, wage employees | 0.01 | −0.54 to 0.52 | 42.4 |

The interval for the employment rate excludes falls larger than 0.1 points. Across the robustness specifications (full sample, national comparison group, comparison municipalities within 200 km of the zone, state × quarter effects, unweighted cells) the estimate ranges from −0.7 to 1.0 points, and none is significantly different from zero. There is no detectable change in formal employment or in the formal share; the point estimates are small and positive, and the intervals include changes of about two points in either direction.

### 4.2 Transitions

*Table 2. Difference-in-differences estimates: quarterly transition rates*

| Transition | Estimate | 90% interval | Pre-period rate, zone |
|---|---|---|---|
| Informal to formal | −0.0124 | −0.0503 to 0.0157 | 0.185 |
| Not employed to formal | 0.0008 | −0.0168 to 0.0121 | 0.067 |
| Formal to informal | −0.0020 | −0.0169 to 0.0103 | 0.104 |
| Formal to not employed | −0.0016 | −0.0144 to 0.0090 | 0.067 |
| Informal to not employed | 0.0029 | −0.0128 to 0.0217 | 0.191 |

The upper end of the interval for the informal-to-formal rate, 1.6 points, is below one tenth of the pre-period rate (1.85 points). The point estimate is negative in the main specification and in all robustness specifications except unweighted cells. No other transition rate changed detectably.

### 4.3 Earnings

The share of wage employees reporting monthly earnings below the new minimum fell by 8.4 points (90% interval −12.0 to −5.4) from 47%. In the event study it falls by 4.1 points in 2019Q1 and by 7.1 to 8.2 points in each later quarter of 2019; a placebo with a false treatment date in 2018Q1 gives −2.5 points (p = 0.45). The decline is larger for workers with less than twelve years of schooling (−11.3 points) than for the rest (−4.8), and similar for women (−9.5) and men (−7.4). The pre-period coefficients of this measure are, however, jointly different from zero (p = 0.031): the share fell faster in the zone than elsewhere in 2016–2017 before stabilising from 2017Q4. Starting the pre-period in 2017Q3, a choice made after seeing the event studies, gives −7.1 points (−11.4 to −3.9).

By earnings bin, wage employees below the minimum fell by 4.0 per 100 persons aged 15 and over (3.2 formal, 0.8 informal) and those at 1.0–1.5 times the minimum rose by 2.4 per 100, all formal. Among formal wage employees, those at 0.6–1.0 times the minimum fell by 3.3 per 100 and those at 1.0–1.5 times rose by 2.5. Informal wage employees below the minimum fell, with no increase above it.

At the same time, the share of wage employees reporting an amount fell by 7.8 points (−13.5 to −2.0) from 77%. The decline appears from 2019Q2 and deepens through the year (−7.1, −9.2 and −11.7 points in 2019Q2–Q4), with no pre-period movement (joint p = 0.72). Wage employees not reporting an amount rose by 3.9 per 100 persons aged 15 and over (2.7 formal, 1.1 informal). Wage employment as a whole did not change significantly, so the fall in jobs below the minimum is matched by the rise just above it and among non-reporters.

Respondents who give no amount are asked whether their income is below, equal to, or in stated multiples of the minimum wage read out by the interviewer, which is the minimum in force where they live. An addendum to the plan, written before these answers were tabulated by zone or period, examined them.

*Table 3. Difference-in-differences estimates: type of earnings answer (share of wage employees)*

| Answer | Estimate | 90% interval | Pre-period mean, zone |
|---|---|---|---|
| Amount | −0.078 | −0.135 to −0.020 | 0.769 |
| Range (codes 1–7) | 0.016 | −0.010 to 0.041 | 0.083 |
| Below the minimum (code 1) | 0.006 | 0.002 to 0.008 | 0.002 |
| Equal to the minimum (code 2) | 0.012 | 0.005 to 0.021 | 0.005 |
| One to two minimums (code 3) | 0.018 | 0.004 to 0.037 | 0.033 |
| No answer (refused, don't know) | 0.063 | 0.016 to 0.104 | 0.148 |

Range answers account for about a fifth of the fall in amounts reported. The increase is at and just above the minimum, in the categories "equal to the minimum" (1.2 points, from 0.5%) and "one to two minimums" (1.8 points); higher categories fell, partly because the yardstick read out had doubled. Most of the fall in reporting is a rise in refusals and "don't know" (6.3 points), whose cause cannot be determined from the survey.

When range answers are added to the bins, each spread uniformly over its interval using the minimum in force for that person and quarter (with "equal to the minimum" as a point), the share of wage employees below the minimum among those giving an amount or a range falls by 11.8 points (−15.5 to −7.4); its pre-period coefficients are not jointly significant (p = 0.18). The corresponding count of wage employees below the minimum falls by 5.6 per 100 persons aged 15 and over (−7.1 to −3.9; formal −4.5, informal −1.1) and that at 1.0–1.5 times rises by 3.5 (2.2 to 5.4; formal 3.3). The pre-period coefficients of the corrected count below the minimum are jointly significant (p = 0.018), so under the plan's rule this estimate cannot support a conclusion. As a description, the remaining rise in non-response (3.0 per 100; 2.2 among formal employees) would reduce the fall below the minimum to 2.6 per 100 for all wage employees, or 2.4 for formal employees, if all of these persons earned less than the minimum.

Mean log hourly earnings of wage employees reporting an amount rose by 1.5% (−1.8 to 6.3), with jointly significant pre-period coefficients (p = 0.045). The estimate is 4.7% (p = 0.01) with a national comparison group and 4.3% (p = 0.001) for workers with less than twelve years of schooling. Hourly earnings of own-account workers rose by 2.9% (−3.9 to 9.2).

### 4.4 Municipalities and distance to the edge of the zone

Municipality maps in the accompanying application show levels before 2019 and changes during 2019 and in 2020Q1 for municipalities with at least 300 person records in each period (16 zone and 42 comparison municipalities for 2019). The fall in the share below the minimum, net of the mean change among comparison municipalities, is between 5 and 19 points in 13 of the 16 zone municipalities shown, including Tijuana, Mexicali, Ensenada, Reynosa, Matamoros and Nogales; the exceptions are Nuevo Laredo (1 point), Juárez (−2) and Tecate (−2). The changes in comparison municipalities are centred on zero, and their variation does not exceed what sampling error would produce: empirical Bayes shrinkage pulls them entirely to the group mean. Plotted against the distance from the municipal centroid to the edge of the zone, the changes are concentrated inside the zone, with no gradient among comparison municipalities within 200 km. The plot is a spatial representation of the difference in differences, not an estimate in its own right; municipalities are large and few lie close to the edge.

### 4.5 Propositions

P32, that the package increased transitions from informal to formal employment, is rejected under the plan's rule, narrowly: the upper end of the 90% interval (1.6 points) is below one tenth of the pre-period rate (1.85 points).

P31, that the package raised low wages without reducing employment, has two readings. The plan's rejection rule applies if the earnings effect is below 2% with an interval that includes zero, which is the case for log hourly earnings (1.5%, −1.8 to 6.3); read literally, P31 is rejected. The plan's §6 also states that an outcome with pre-trends is unreliable, and log earnings have jointly significant pre-period coefficients. Applying §6 before the rejection rule, as decided after the results were seen (D-055), leaves P31 inconclusive. The employment component of P31 is met in either reading.

P33, that informal wages also moved (fewer informal jobs below the minimum), meets its support rule (−0.8 per 100, interval −1.6 to −0.1) but depends on the earnings bins, which §6 treats as unreliable when reporting changes by more than three points; it is therefore inconclusive. There is no increase in informal jobs above the minimum.

## 5. Limitations

The VAT and income-tax reductions in the zone may have offset part of the cost of the higher minimum wage, so the employment effects of a minimum-wage increase alone could be less favourable.

The pre-trends in the earnings measures limit what can be concluded about the size of the wage effect. The 2019 decline in the share below the minimum is larger than any pre-period movement after 2017, but the uncorrected and corrected counts of jobs below the minimum both fail the pre-trend test.

The fall in earnings reporting is mostly refusals and "don't know", whose cause is not established. Spreading range answers uniformly within their intervals is an assumption; for codes 1 and 2 it does not affect on which side of the minimum an answer falls.

The full sample, including the units added in 2019, gives almost identical estimates (−8.0 points for the share below the minimum, 0.8 for the employment rate).

With about thirty treated municipalities and one year after the change, effects on transitions of a few points a quarter cannot be excluded.

## 6. Conclusions

The 2019 package of a doubled minimum wage and lower taxes in Mexico's northern border zone did not reduce employment and did not detectably increase transitions from informal to formal employment within a year. The distribution of reported earnings among formal wage employees shifted from just below to just above the new minimum, consistent with administrative evidence; the size of this shift cannot be pinned down with the survey, because earnings reporting fell in the zone at the same time and because the count-based measures fail the pre-trend test. For evaluations of the policy with ENOE, both the 2019 sample expansion in the zone and the fall in reporting need to be taken into account.

## Annex A. Implementation notes and further work

Design checks made before estimation used no outcomes: counts of records and sampling units by quarter and group, which revealed the 2019 expansion; the match of the list of zone municipalities to INEGI codes (the list was compiled from the minimum-wage resolution and checked against ENOE's zone variable, which marks only listed municipalities); and municipality codes, which are stored with leading spaces in some files. Records with no municipality code, about 1% a quarter and outside the self-represented cities, are excluded.

Choices made after the results were seen (D-055): the plan's §6 applied mechanically to the propositions; bounds on missing jobs under extreme assumptions about non-reporters; a pre-period starting in 2017Q3; Baja California Sur added to the geometry to locate the zone's southern edge; fit lines in the distance plot limited to the observed range. Addendum A1 (D-056) added the analysis of range answers before they were tabulated by zone or period; its hypothesis H-A (most of the fall in reporting is range answers) is inconclusive and H-B (the rise in range answers is concentrated at "equal to the minimum") is supported by its rule, although the rise in "one to two minimums" is larger. The comparison of existing and added sampling units in 2019 (§2) was carried out after the independent audit of the programme (D-064).

The plan's individual-level regression with the same fixed effects was not estimated. Earnings bins based on hourly earnings were computed but are not comparable with the monthly bins, because their threshold (the daily minimum divided by eight hours) does not correspond to the monthly minimum for a 48-hour week; they are left in the output files. Map cells require 300 unweighted person records. Some 2016–2019 ENOE files begin with a UTF-8 byte-order mark, which the reader now strips.

Municipal values in the maps are ratio estimates with variances from a bootstrap over primary sampling units within the municipality (200 replications). Changes are net of the population-weighted mean change among comparison municipalities and are shrunk towards the mean of the municipality's group by a method-of-moments empirical Bayes estimator. The variances of changes ignore the positive covariance from repeated interviews of the same dwellings, so the shrinkage is conservative.

Further work could examine who refuses to report earnings and whether refusals cluster by area (open question OQ-73); link formal hires to IMSS records to test transitions out of informality with administrative data; extend the analysis to 2020Q3–2023 with ENOE^N, modelling the 2020–2023 increases in both regions; and use price data to separate the tax reductions.

Correction of 2026-11-16 (D-069): the fixed-effects projection used in all estimates was replaced by a pivoted QR decomposition after it was found to give incorrect coefficients when the fixed effects contain several linear dependencies. Only the robustness specification with state × quarter effects is affected; its estimates change slightly (for example, the informal-to-formal transition rate from −1.9 to −2.3 points), and the statements above about that specification are unchanged.

## References

Alvarado Pérez, R., Orraca Romano, P.P. and Cabrera-Hernandez, F. (2023). El efecto de duplicar el salario mínimo en la brecha de género en empleo y salarios en México. *El Trimestre Económico* 90(360): 961–999. [L151]

Cabrera-Hernandez, F. and Duval-Hernández, R. (2026). Minimum wage and job transitions in Mexico. IZA Discussion Paper 18443. [L152]

Cameron, A.C., Gelbach, J.B. and Miller, D.L. (2008). Bootstrap-based improvements for inference with clustered errors. *Review of Economics and Statistics* 90(3): 414–427. [L155]

Campos-Vázquez, R.M. and Esquivel, G. (2021). The effect of doubling the minimum wage on employment and earnings in Mexico. *Economics Letters* 209: 110124. [L150]

Cengiz, D., Dube, A., Lindner, A. and Zipperer, B. (2019). The effect of minimum wages on low-wage jobs. *Quarterly Journal of Economics* 134(3): 1405–1454. [L153]

Decreto de estímulos fiscales región fronteriza norte. *Diario Oficial de la Federación*, 31 December 2018. [L154]

MacKinnon, J.G. and Webb, M.D. (2018). The wild bootstrap for few (treated) clusters. *Econometrics Journal* 21(2): 114–135. [L156]
