# Job Transitions by Sector, Establishment Size and Formality in Mexico, 2018–2024

*Paul Wander. Working draft v0.3, 2026-11-16. Pre-analysis plan: [`00_pre_analysis_plan.md`](00_pre_analysis_plan.md). Generated tables: [`empirics/output/enoe/ladders/results.md`](../../../empirics/output/enoe/ladders/results.md). App: Jobs in Mexico, page 9.1.*

## Abstract

Using the rotating panel of Mexico's labour-force survey (ENOE), this paper follows persons aged 16–65 employed at a first interview to their fifth interview, one year later, in two windows (2018Q4–2019Q4 and 2023Q1–2024Q1). It asks whether the sector of a job, or the size class and formality of the establishment, better predicts two outcomes: exit to non-employment, and a move to a job cell with higher median hourly earnings. In a Shapley decomposition of the explained variance, establishment size × formality accounts for more than sector of both outcomes, by 0.9–1.4 points of R² for exits and 3.5–4.3 points for upward moves, but the two groupings together explain only 3% and 7% of the variance. The advantage for exits disappears when transitions must be confirmed at an adjacent interview. The advantage for upward moves depends on establishment size, which a third of employees with the same employer report differently a year later. When upward moves must involve a change of employer, as the plan requires given this reporting error, the advantage is 0.5 points (90% interval 0.3–0.9), in 2023–24 only. Within establishment size × formality cells, manufacturing jobs show more upward moves than service jobs, but the difference disappears when the earnings rank of the starting job is held constant.

## 1. Introduction

Cross-country work on sectors as motors of growth, including this project's replication of Szirmai and Verspagen (2015) in WP07, treats each sector as uniform. Productivity differences within sectors, between formal and informal producers or between large and small establishments, are larger than those between sectors (WP06, WP08). This paper takes the job as the unit of analysis and asks, following Donovan, Lu and Schoellman (2023), whether particular kinds of job lead to stable and better-paid employment.

The hypothesis stated before the data were examined (proposition P-RG3) is that establishment size and formality predict these outcomes better than sector does. A second rejection condition in the plan asks whether, within establishment size × formality cells, manufacturing jobs have lower exit rates and more upward moves than service jobs, in which case sector would remain the more useful unit.

## 2. Data

ENOE interviews each sampled dwelling in five consecutive quarters and replaces one fifth of the sample each quarter. The paper uses two windows of five quarters, 2018Q4–2019Q4 before the pandemic and 2023Q1–2024Q1 after the 2020 redesign of the survey. The sample consists of persons aged 16–65 with complete interviews who are usual or new residents.

Persons are linked across consecutive quarters by INEGI's dwelling, household and person identifiers, with the visit number rising by one; links are accepted when sex is unchanged and age changes by −1 to +2 years. In the 2023–24 files the dwelling identifier must include the variable TIPO, without which 10–13% of identifiers are shared by two households. Of those who could be followed to the next quarter, 91.5–93.1% are linked in 2018–19 and 88.1–90.2% in 2023–24.

Jobs are described by sector (11 groups, INEGI's `rama_est2`), establishment size class (`ambito2`: micro without and with premises, small, medium, large, government, and a residual category) and formality (INEGI's labour-informality definition). The residual size category includes `ambito2` code 0, which INEGI uses for agriculture and for establishments of unspecified size; 57–63% of workers in that category are in agriculture. Survey weights at the first interview are used, and intervals come from a bootstrap that resamples primary sampling units within states (499 replications).

## 3. Measurement

The population is persons employed at the first interview and observed at the fifth. The outcomes are exit, being not employed one year later; an upward move, being employed one year later in a job cell (sector × size × formality) whose median hourly earnings at the first interview exceed those of the starting cell; and an upward move with a change of employer, identified from the reported start date with the current employer, which is asked only in first quarters and therefore exists only for 2023–24. Cells with fewer than the minimum number of observations are pooled within sector and formality into a residual size cell; median earnings are computed on the unpooled cells and include employers.

For each outcome, the variance explained by sector indicators and by size × formality indicators is split with a Shapley decomposition of the R² of weighted regressions on the two sets of indicators, and the difference between the two shares is reported with a bootstrap interval.

## 4. Results

### 4.1 Flows in and out of employment

*Table 1. Quarterly transition rates*

| | Leaving employment | Finding employment | Changing employer (employees) |
|---|---|---|---|
| Whole country, 2018–19 | 0.124 | 0.216 | 0.060 |
| Whole country, 2023–24 | 0.116 | 0.213 | 0.056 |
| Self-represented cities, 2018–19 | 0.117 | 0.213 | 0.046 |
| Self-represented cities, 2023–24 | 0.108 | 0.208 | 0.045 |

Rates are shares of the relevant population from one quarter to the next. Changing employer is measured between a fourth and the following first quarter, for employees with less than three months with their current employer. A comparison with Donovan, Lu and Schoellman's estimates for Mexico requires their replication files and has not been made.

### 4.2 Sector against establishment size and formality

*Table 2. Shapley share of size × formality minus that of sector (90% interval); positive values favour size × formality*

| Outcome | 2018–19 | 2023–24 |
|---|---|---|
| Exit within a year | 0.014 (0.010 to 0.019) | 0.009 (0.005 to 0.014) |
| Upward move | 0.035 (0.026 to 0.042) | 0.043 (0.035 to 0.052) |
| Upward move with a change of employer | — | 0.005 (0.003 to 0.009) |

In this specification size × formality explains more of both outcomes than sector does. The explained shares are small: the two groupings together explain 3% of the variance of exits and 7% of the variance of upward moves. Excluding workers who start in agriculture, so that the residual size category no longer stands in for a sector, raises the differences for exits to 0.019 and 0.013 and for upward moves to 0.051 and 0.065. Exit rates within a year range from 5.5% to 10.6% across formal size classes and from 10.9% to 23.1% across informal ones.

### 4.3 Manufacturing and services within size × formality cells

*Table 3. Manufacturing minus services within size × formality cells (90% interval)*

| Outcome | 2018–19 | 2023–24 | Mean in services |
|---|---|---|---|
| Exit within a year | 0.022 (0.000 to 0.043) | 0.017 (−0.001 to 0.034) | 0.16 / 0.15 |
| Upward move | 0.049 (0.023 to 0.074) | 0.092 (0.068 to 0.117) | 0.25 / 0.24 |
| Upward move, holding the starting cell's earnings rank constant | −0.008 (−0.038 to 0.025) | 0.027 (−0.002 to 0.055) | |
| Upward move with a change of employer | — | 0.014 (0.002 to 0.025) | 0.04 |
| Same, holding the starting cell's earnings rank constant | — | 0.001 (−0.012 to 0.013) | |

The comparison controls for size × formality, age group, sex and schooling. Without a control for the earnings rank of the starting cell, manufacturing jobs are followed by moves to better-paid cells more often than service jobs. Manufacturing cells, however, start lower on average in the ranking of cells by median earnings, which leaves more room for an upward move by construction. Holding the rank decile constant, an analysis added after the independent audit of the programme (D-064), the difference is close to zero in 2018–19 and smaller and not significant in 2023–24, and the difference in moves with a change of employer disappears. Manufacturing jobs are not more stable: their exit rates are, if anything, higher.

### 4.4 Transitions between informal and formal employment

*Table 4. State one year later by state at the first interview, 2023–24*

| | Not employed | Informal | Formal |
|---|---|---|---|
| Not employed | 0.748 | 0.186 | 0.067 |
| Informal | 0.175 | 0.680 | 0.145 |
| Formal | 0.083 | 0.149 | 0.768 |

The 2018–19 matrix is similar, with an informal-to-formal rate of 0.130. About one informal worker in seven is formally employed a year later and one formal worker in seven informally employed; among persons not employed who find work within the year, about three in four enter informal jobs. These are gross flows, part of which is reporting error (Section 5.1).

### 4.5 Earnings growth

Hourly earnings are reported at both interviews by between 37% and 71% of workers employed at both, depending on the size × formality cell. Among those who report, median nominal growth over a year is generally higher for those who remain in the same job cell than for those who move, with exceptions in each window. Given the non-response and the absence of a price deflator, differences between cells are not interpreted.

### 4.6 Proposition

The plan's rule makes the comparison under confirmed transitions decisive and classes the result as inconclusive if the two outcomes give different answers. Under confirmed transitions, size × formality has no advantage for exits (−0.004 and 0.000) and an advantage for upward moves (0.024 and 0.039). With upward moves redefined on changes of employer, as the plan requires once more than 10% of same-employer workers report a different size class, the advantage is 0.005 (0.0002 to 0.011) under confirmed transitions in 2023–24. P-RG3 is therefore inconclusive. The second rejection condition is not met: manufacturing jobs do not have lower exit rates, and their higher rate of upward moves does not survive the control for the starting cell's earnings rank.

## 5. Robustness

### 5.1 Reporting error

Among 2,300 employees who reported the same start date with their employer in 2023 and in 2024, 34% reported a different establishment size class and 8.7% a different formality status. Some establishments cross a size boundary within a year, but most of this change must be reporting error, which creates spurious transitions. Three checks are applied: keeping only persons whose states at the first and fifth interviews are repeated at the adjacent interview (confirmed transitions); excluding answers given by another household member (self-reports); and counting upward moves only when they involve a change of employer (2023–24). Under confirmed transitions the size × formality advantage for exits disappears (−0.004, interval −0.015 to 0.010, in 2018–19; 0.000, −0.008 to 0.007, in 2023–24). For upward moves the advantage remains positive in each check, although for moves with a change of employer among self-reports the lower end of the interval is zero.

### 5.2 Formality without establishment size

*Table 5. Shapley share of formality minus that of sector (90% interval); negative values favour sector*

| Outcome | 2018–19 | 2023–24 | 2023–24, confirmed transitions |
|---|---|---|---|
| Exit within a year | 0.012 (0.007 to 0.015) | 0.008 (0.002 to 0.011) | −0.008 (−0.020 to −0.004) |
| Upward move | −0.023 (−0.029 to −0.019) | −0.009 (−0.015 to −0.006) | −0.009 (−0.019 to −0.006) |
| Upward move with a change of employer | — | −0.001 (−0.005 to 0.002) | 0.000 (−0.005 to 0.001) |

Without establishment size, sector explains as much of upward moves as formality or more. The advantage of size × formality for upward moves therefore comes from establishment size, the dimension reported with most error; misreported size moves workers between cells with different median earnings, so part of that advantage may be an artefact. For exits, formality alone explains more than sector in the simplest specification and less once transitions are confirmed.

### 5.3 Attrition

Persons who leave the dwelling cannot be followed. Reweighting the linked sample so that it matches, by age group × sex × labour-force status at the first interview, everyone who could have been followed for a year changes every Shapley difference by less than 0.001, the transition matrices by at most 0.003 and the manufacturing–services differences by less than 0.002.

## 6. Conclusions

The evidence does not establish that establishment size and formality, rather than sector, distinguish jobs that lead to stable and better-paid employment in Mexico. Formality predicts exits, but its advantage over sector disappears once spurious transitions are removed; establishment size predicts upward moves, but it is reported so inconsistently that this may be partly an artefact, and without it sector does as well as formality. The higher rate of upward moves from manufacturing jobs reflects their lower starting position in the earnings ranking.

The more robust finding concerns magnitudes: the characteristics of jobs recorded in a labour-force survey explain a small part of what happens to individual workers within a year. Whatever distinguishes jobs that lead somewhere is likely to lie in characteristics these surveys do not record well, such as the employer, the occupation within the establishment and the worker's skills, which points to linked employer–employee data such as IMSS records and to horizons longer than ENOE's rotation allows. The results are descriptive; persons are not assigned to jobs at random, and the controls capture only part of the differences between them.

## Annex A. Implementation notes and further work

The main estimates use first-interview survey weights; the plan specified weights adjusted for attrition, which are reported as a robustness check (Section 5.3) because the first estimates were produced before the adjustment was implemented.

Choices made after examining the data (D-047, D-048): TIPO included in the dwelling identifier for 2023–24; the interview month for 2018–19 taken from the interview-week field, which for records outside the self-represented cities does not identify the week, so that the first month of the quarter is assigned (the effect on the job-to-job rate is in the fifth decimal place); employer change identified from the start date, with workers who started before the previous year classed as having the same employer; and an exploratory decomposition conditional on the origin cell's earnings-rank decile, in which size × formality still explains more of upward moves (0.029 and 0.015).

Departures from the plan not described in the first version and disclosed after the independent audit (D-064): small cells are pooled into a residual size cell within sector and formality (20% of the sample) instead of being merged with the nearest size class; earnings ranks are computed on unpooled cells, 20 of about 110 of which have fewer than ten earners, and include employers; the primary sampling unit is the UPM alone rather than CA + UPM; the plan's §5.5 redefinition of upward moves on employer changes is presented alongside, rather than instead of, the original outcome; and several planned items were not produced (intervals for rates by cell, the variant with ages 15+, separate unemployment and inactivity, the seven-sector mapping, the control for interview mode, and the urban version of the decomposition). The size label "other" also covers INEGI's code 0; the decomposition without agricultural origins (Section 4.2) and the manufacturing comparison conditional on the earnings rank (Section 4.3) were added after the audit.

Further work could define outcomes on employers using linked employer–employee records; impute missing hourly earnings or use INEGI's income ranges; compare the flows with Donovan, Lu and Schoellman's estimates for Mexico; and repeat the exercise with other rotating panels in the region (Brazil's PNAD Contínua; Argentina's EPH).

## References

Donovan, K., Lu, W.J. and Schoellman, T. (2023). Labor market dynamics and development. *Quarterly Journal of Economics* 138(4): 2287–2325. [L160]

Szirmai, A. and Verspagen, B. (2015). Manufacturing and economic growth in developing countries, 1950–2005. *Structural Change and Economic Dynamics* 34: 46–59. [L120]
