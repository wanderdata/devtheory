# Which Jobs Are Rungs? Labour-Market Flows by Sector, Firm Size and Formality in Mexico

*Paul Wander. Working draft v0.2, 2026-11-13. Pre-analysis plan: [`00_pre_analysis_plan.md`](00_pre_analysis_plan.md). Generated tables: [`empirics/output/enoe/results.md`](../../empirics/output/enoe/results.md). Dashboard: productivity app, page "Job ladders in Mexico".*

## Abstract

Using the rotating panel of Mexico's labour force survey (ENOE), we follow workers aged 16–65 for a year in two windows, 2018–19 and 2023–24. We ask which characteristics of a job predict whether its holder stays employed and moves to better-paid work: the job's sector, or the size and formality of the firm.

Firm size and formality together account for more of the variation in upward moves than sector does, and for more of the variation in exits in the simplest specification. Both advantages weaken under scrutiny:
- **Exits.** For exits to non-employment, the advantage disappears when transitions must be confirmed at a later interview.
- **Upward moves.** For upward moves, it rests on firm size. A third of employees who stay with the same employer report a different firm-size class a year later. With formality alone, sector explains upward moves as well or better.

Within the same type of firm, manufacturing jobs lead more often than service jobs to better-paid work, but they are not more stable. Whatever the grouping, the characteristics of the job explain only 1–7% of individual outcomes within a year.

## 1. Introduction

Cross-country work on "motors" of growth, including our own replication of Szirmai and Verspagen (WP07), looks for sectors whose expansion raises aggregate growth. That search treats each sector as uniform. Productivity differences within a sector, between a formal exporter and an informal workshop, are larger than those between sectors (WP06, WP08). This paper moves the unit of analysis to the job. Following Donovan, Lu and Schoellman (2023), it asks whether a job works as a rung, leading to stable and better-paid employment, or as a dead end.

The question is which characteristics of a job predict rung behaviour in Mexico. The hypothesis, stated before the data were examined, is that firm size and formality predict it better than sector (proposition P-RG3).

## 2. Data

**Survey.** ENOE interviews each sampled dwelling in five consecutive quarters, replacing one fifth of the sample every quarter. We use two windows of five quarters:
- **2018 Q4–2019 Q4**, before the pandemic;
- **2023 Q1–2024 Q1**, after the survey's 2020 redesign.

**Sample.** Persons aged 16–65 with complete interviews who are usual or new residents.

**Linking.** Persons are linked across consecutive quarters by INEGI's dwelling, household and person identifiers, with the visit number rising by one. Links are accepted when sex is unchanged and age changes by −1 to +2 years. In the 2023–24 files the dwelling identifier must include the variable TIPO, without which 10–13% of identifiers are shared by two households. Of those who could be followed to the next quarter:
- 91–93% are linked in 2018–19;
- 88–90% are linked in 2023–24.

**Variables:**
- **Job characteristics:** sector (11 groups, INEGI's `rama_est2`), firm-size class (`ambito2`: micro without or with premises, small, medium, large, government, other) and formality (INEGI's labour-informality definition: no access to social security through the job, or work in an informal unit).
- **Weights:** first-interview survey weights.
- **Inference:** intervals come from a bootstrap that resamples primary sampling units within states (499 replications).

## 3. Measuring job ladders

**Population.** People employed at the first interview who are observed again at the fifth, one year later.

**Outcomes:**
- **exit:** not employed one year later;
- **upward move:** employed one year later in a job cell (sector × firm size × formality) whose median hourly earnings at the first interview were higher than those of the original cell;
- **upward move with a new employer:** an upward move that involves a change of employer, identified from the start date with the current employer. This question is asked only in first quarters, so the outcome exists only for 2023–24.

**Comparing the two groupings.** For each outcome, the variance explained by sector and by firm size × formality is split with a Shapley decomposition of the R² from weighted regressions on the two sets of indicators.

## 4. Results

### 4.1 Flows in and out of work

Quarterly flows are of the size found for middle-income countries.

| | Leaving employment | Finding employment | Changing employer (employees) |
|---|---|---|---|
| Whole country, 2018–19 | 0.124 | 0.216 | 0.060 |
| Whole country, 2023–24 | 0.116 | 0.213 | 0.056 |
| Self-represented cities, 2018–19 | 0.117 | 0.213 | 0.046 |
| Self-represented cities, 2023–24 | 0.108 | 0.208 | 0.045 |

Shares of the relevant population, quarter to quarter. "Changing employer" is measured between a fourth quarter and the following first quarter, for employees with less than three months with their current employer.

### 4.2 Sector versus firm size and formality

The table gives the Shapley share of firm size × formality minus that of sector, with 90% intervals; positive values favour firm size × formality.

| Outcome | 2018–19 | 2023–24 |
|---|---|---|
| Exit within a year | +0.014 [+0.010, +0.019] | +0.009 [+0.005, +0.014] |
| Upward move | +0.035 [+0.027, +0.042] | +0.043 [+0.035, +0.052] |
| Upward move with a new employer | — | +0.005 [+0.003, +0.009] |

In this specification firm size × formality explains more of both outcomes. The shares themselves are small. Sector and firm size × formality together explain 3% of the variance of exits and 7% of the variance of upward moves. Section 5 shows how much of this survives checks on reporting error.

**Exit rates by type of firm.** Formal jobs end in non-employment within a year far less often than informal ones:
- **formal:** 5–11%, depending on firm size and window;
- **informal:** 11–23%.

### 4.3 Manufacturing and services within the same type of firm

Comparing manufacturing with services (commerce, restaurants and accommodation, transport and communications, professional, social and other services) within the same firm size × formality cell, controlling for age group, sex and schooling:

| Outcome | 2018–19 | 2023–24 | Mean in services |
|---|---|---|---|
| Exit within a year | +0.022 [+0.000, +0.044] | +0.017 [−0.001, +0.034] | 0.15 |
| Upward move | +0.049 [+0.023, +0.075] | +0.092 [+0.068, +0.117] | 0.24 |
| Upward move with a new employer | — | +0.014 [+0.002, +0.025] | 0.04 |

Manufacturing jobs lead to better-paid cells more often than service jobs in the same type of firm, including through a change of employer (1.4 points on a base of 4). They are not more stable; if anything, exits are slightly more frequent. On this evidence manufacturing works as a rung, from which workers move up, more than as a destination. This is consistent with WP07's finding that manufacturing's share of employment, not of output, is associated with growth.

### 4.4 Moving between informal and formal work

Rows give the state at the first interview; columns give the state one year later.

| 2023–24 | Not employed | Informal | Formal |
|---|---|---|---|
| Not employed | 0.748 | 0.186 | 0.067 |
| Informal | 0.175 | 0.680 | 0.145 |
| Formal | 0.083 | 0.149 | 0.768 |

The 2018–19 matrix is almost the same; the informal-to-formal rate was 0.130 then.

- **Persistence.** About one informal worker in seven is in formal work a year later, and one formal worker in seven is in informal work. Two-thirds of informal workers remain informal.
- **Entry.** Among people not employed who find work within the year, nearly three in four enter informal jobs.

These are gross flows. Part of the movement between formal and informal is reporting error (Section 5.1).

### 4.5 Earnings growth

**Coverage.** Hourly earnings are reported at both interviews by only 45–60% of workers employed at both, depending on the type of job.

**Pattern.** Among those who report, median nominal growth over a year is generally higher for those who stay in the same job cell than for those who move. There are exceptions, among them informal micro-firms with premises in 2018–19 and medium-sized formal firms in 2023–24. Given the non-response and the absence of a price deflator, we do not interpret differences between cells.

## 5. Robustness

### 5.1 Reporting error

Among 2,300 employees who gave the same start date with their employer in 2023 and in 2024:
- **firm size:** 34% reported a different firm-size class;
- **formality:** 8.7% reported a different formality status.

Some firms grow across a size boundary in a year, but most of the change in reported size must be error. Misreporting creates spurious transitions, so we apply three checks:
1. **Confirmed transitions.** Keep only people whose state at the first and fifth interviews is repeated at the adjacent interview.
2. **Self-reports.** Exclude answers given by another household member.
3. **New employer.** Measure upward moves only when they involve a change of employer (2023–24).

Under confirmed transitions, firm size × formality no longer explains more of exits than sector:
- **2018–19:** −0.004 [−0.015, +0.010];
- **2023–24:** +0.000 [−0.008, +0.007].

For upward moves the advantage remains in every check.

### 5.2 Formality without firm size

Given how poorly firm size is reported, the decomposition was repeated with formality alone. Values are the Shapley share of formality minus that of sector; negative values favour sector.

| Outcome | 2018–19 | 2023–24 | 2023–24, confirmed transitions |
|---|---|---|---|
| Exit within a year | +0.012 [+0.007, +0.015] | +0.008 [+0.002, +0.011] | −0.008 [−0.020, −0.004] |
| Upward move | −0.023 [−0.029, −0.019] | −0.009 [−0.015, −0.006] | −0.009 [−0.019, −0.006] |
| Upward move with a new employer | — | −0.001 [−0.005, +0.002] | −0.000 [−0.005, +0.001] |

- **Upward moves.** Without firm size, sector explains as much as formality or more. The advantage of firm size × formality for upward moves therefore comes from firm size, the dimension reported with most error. Misreported size moves workers between cells with different median earnings, so part of that advantage may be an artefact.
- **Exits.** Formality alone explains more than sector in the simplest specification and less once transitions are confirmed.

### 5.3 Attrition

People who leave the dwelling between interviews cannot be followed. To check whether this matters, the linked sample was reweighted so that, by age group × sex × labour-force status at the first interview, it matches everyone who could have been followed for a year. Every Shapley difference changes by less than 0.001, the transition matrices by less than 0.002, and the manufacturing–services differences by less than 0.002.

## 6. Conclusions

The evidence does not settle whether firm size and formality, rather than sector, distinguish rungs from dead ends in Mexico.
- **Exits.** Formality predicts exits, but the advantage over sector disappears once spurious transitions are removed.
- **Upward moves.** Firm size predicts upward moves, but firm size is reported so inconsistently that this may be partly an artefact. Without it, sector does as well as formality.
- **Manufacturing.** Manufacturing jobs show more upward movement than service jobs in the same type of firm, but not more stability.

The more robust conclusion concerns magnitudes. Any grouping of jobs available in a labour-force survey explains a small part of what happens to individual workers within a year. Ladders, if they operate, do so through characteristics these surveys do not record well: the employer, the occupation within the firm, and the worker's skills. That points toward linked employer–employee data, such as IMSS administrative records for formal employment, and toward longer horizons than ENOE's rotation allows.

These are descriptive results. People are not assigned to jobs at random, and the controls capture only part of the differences between those who hold different jobs.

## Annex A. Notes on implementation and further work

**A.1 Weights.** The main estimates use first-interview survey weights. The plan specified weights adjusted for attrition, by age group × sex × labour-force status, following Donovan, Lu and Schoellman. These are reported as a robustness check in Section 5.3, because the first estimates were produced before the adjustment was implemented. A fuller check would rake on more margins (state, schooling, firm type) or model the probability of being re-interviewed. That matters most for young workers, who leave the parental dwelling and drop out of the panel.

**A.2 Benchmark.** The flows in Section 4.1 should be compared with Donovan, Lu and Schoellman's estimates for Mexico (1995–2017). This requires their replication package.

**A.3 Choices made after examining the data.**
- **TIPO in the dwelling identifier.** Required for 2023–24, without which identifiers were duplicated.
- **Interview month for 2018–19.** Taken from the interview-week field, because those files lack the month.
- **Employer change.** Identified from the start date. The month is asked only of workers who started in the current or previous year, so earlier starters are classed as having the same employer.
- **Upward moves with a new employer.** Applied because more than 10% of same-employer workers report a different firm size, a threshold set in the plan.
- **Exploratory variant.** A decomposition conditional on the origin cell's earnings-rank decile allows for the ceiling on upward moves from well-paid cells. Firm size × formality still explains more (+0.029 and +0.015, both intervals above zero).

These choices are recorded in the project's decision log (D-047, D-048).

**A.4 Further needs.**
- **Employer identifier.** Linked employer–employee records would allow the outcomes to be defined on employers rather than reported firm size.
- **Hourly earnings.** Imputing missing hourly earnings, or using INEGI's income ranges, would make Section 4.5 usable.
- **Longer histories.** Other countries' rotating panels with longer follow-up (Brazil's PNAD Contínua, five consecutive quarters; Argentina's EPH, whose 2-2-2 rotation spans a year and a half) would allow the same exercise elsewhere in the region.
