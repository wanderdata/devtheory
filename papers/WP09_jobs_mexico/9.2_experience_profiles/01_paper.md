# Which Jobs Build Skills? Experience–Earnings Profiles by Type of Job in Mexico, 2005–2025

*Paul Wander. Working draft v0.1, 2026-11-13. Pre-analysis plan: [`00_pre_analysis_plan.md`](00_pre_analysis_plan.md). Generated tables: [`empirics/output/enoe/profiles/results.md`](../../../empirics/output/enoe/profiles/results.md). App: Jobs in Mexico, page 9.2.*

## Abstract

Wages rise much less with experience in poor countries than in rich ones. We ask whether Mexico's flat experience–earnings profile is general or concentrated in particular types of job, using 21 annual cross-sections of the national labour-force survey (ENOE, 2005–2025).

**Size.** Among full-time male private-sector employees, those with 20–24 years of potential experience earn 26% more per hour than entrants. The figure is 25% in formal jobs and 16% in informal jobs, against about 89% in rich countries.

**Formality versus sector.** Within the same sector, formal and informal profiles are almost identical. Differences across sectors, from 15% in agriculture and mining to 36% in professional, financial and social services, are larger than the difference by formality. The national profile is not flat because of where workers are employed: the formal profile is as flat as the national one.

**Trend.** Formal profiles have flattened since the mid-2000s, from 36% to 19%, while informal profiles have stayed near 15%.

**Cohort adjustment.** The method of Lagakos et al. (2018) produces implausible results in these data. We explain why, and base conclusions on cross-sectional profiles.

## 1. Introduction

Lagakos, Moll, Porzio, Qian and Schoellman (2018; hereafter LMPQS) document that experience–wage profiles are about twice as steep in rich countries as in poor ones. For Mexico, on census data for 1990–2010, wages at 20–24 years of experience are 41% above those of entrants, against 89% on average in six rich countries. The result is read as evidence that workers in poor countries accumulate less human capital over their careers. It raises a question LMPQS do not address: which jobs, if any, offer the learning that most jobs in a poor country do not?

The question matters for this project. The search for sectors that act as "motors" of growth (WP07) and the evidence that sector averages hide most productivity dispersion (WP06, WP08) point toward jobs as the relevant unit. One property a motor job should have is that it builds skills: its holders' earnings rise with experience.

Two hypotheses were set out before estimation:
- **P28:** profiles are much steeper in formal than in informal jobs, and the formality gap exceeds differences across sectors.
- **P29:** much of the flatness of the national profile reflects the type of job workers hold at each stage of their careers.

Both are rejected.

## 2. Data

**Survey.** ENOE, first quarter of each year from 2005 to 2025.

**Sample.** The baseline follows LMPQS: men, full-time (35 or more hours a week), private-sector wage employees with positive hourly earnings and 0–40 years of potential experience. Potential experience is age − 18 for those with fewer than 12 years of schooling, and age − schooling − 6 otherwise. The sample has 859,695 observations.

**Formality.** INEGI's labour-informality definition: no social security through the job, or work in an informal unit.

**Sectors.** Six groups formed from INEGI's eleven.

**Firm size.** Two classes, at most and more than ten workers. Study 9.1 found firm size to be reported with substantial error.

**Earnings reporting.** The share of baseline workers reporting positive hourly earnings fell over the period:
- **formal:** from 90% in 2005 to 57% in 2025;
- **informal:** from 93% to 70%.

Within an experience bin, the formal–informal difference in reporting is at most 12 percentage points.

## 3. Method

**Cross-sectional profiles.** Log hourly earnings are regressed on dummies for five-year experience bins and on year dummies, pooled over 2005–2025 with survey weights. The height of a profile at bin *b* is exp(coefficient) − 1 relative to the 0–4 bin; we report heights at 20–24 years. Intervals come from a bootstrap that resamples primary sampling units within state and year (199 replications).

Cross-sectional profiles combine experience effects with differences between birth cohorts. LMPQS separate the two with the Heckman–Lochner–Taber (HLT) restriction: no experience effects in the last ten years of a career, so that wage growth among those workers identifies time effects. We apply it with single-year birth cohorts (Annex A).

**Within-person profiles.** We also compute one-year earnings growth from the linked panels of study 9.1. Growth by experience bin is net of the growth of workers in the 30–39-year bin of the same type of job.

**Composition decomposition.** With informal shares s₀ and s₂₀ at 0–4 and 20–24 years, profile heights c_F and c_I (in logs), and an informal–formal earnings gap g₀ at entry, mean log earnings imply exactly:

national height − formal height = s₂₀(c_I − c_F) + (s₂₀ − s₀)·g₀

The first term is the effect of flatter informal profiles; the second the effect of the informal share changing with experience.

## 4. Results

### 4.1 Flat profiles in every type of job

| Group | Height at 20–24 years | 90% interval | Observations |
|---|---|---|---|
| All baseline workers | 25.7% | 24.9–26.4% | 859,695 |
| Formal | 25.4% | 24.5–26.4% | 506,847 |
| Informal | 15.6% | 14.8–16.4% | 352,848 |
| Firms with more than 10 workers | 30.6% | 29.1–32.0% | 295,855 |
| Firms with up to 10 workers | 24.6% | 23.7–25.6% | 436,777 |
| Women (otherwise baseline) | 16.8% | 15.9–17.6% | 469,198 |
| Own-account men, all hours | −9.4% | −12.1 to −7.0% | 227,334 |

**Level.** The national figure of 26% is lower than LMPQS's 41% for 1990–2010. Part of the difference may come from the source (census against labour-force survey) and part from the flattening documented in Section 4.4.

**Shape.** Profiles peak at 20–29 years of experience and decline afterwards: the baseline height falls to 16% at 35–39 years.

**Formal jobs.** Formal jobs, the best case in Mexico, reach a quarter of entry earnings after twenty years. That is less than a third of the rich-country figure.

**Own-account workers.** Their earnings fall with experience.

### 4.2 Sector matters more than formality

| Sector | Height at 20–24 years |
|---|---|
| Professional, financial and social services | 35.6% |
| Commerce | 29.4% |
| Manufacturing | 27.9% |
| Transport, restaurants and other services | 24.1% |
| Construction | 21.4% |
| Agriculture and mining | 14.6% |

Within the two sectors with enough informal wage employees to estimate both profiles, formality makes no difference:

| | Formal | Informal |
|---|---|---|
| Manufacturing | 22.7% | 22.9% |
| Commerce | 24.0% | 23.3% |

The formal–informal gap in the pooled sample (9.8 points) therefore reflects which sectors formal and informal jobs are in. The sector range (21 points) exceeds the formality gap, so P28 is rejected under the rule stated in the plan, even though the pooled formal profile is 1.6 times as steep as the informal one. Profiles are steeper in firms with more than ten workers (31%) than in smaller ones (25%), with the caveat about how firm size is reported.

### 4.3 The national profile is not flat because of composition

At 0–4 years of experience, 54% of baseline workers are informal; at 20–24 years, 44%. Informal entrants earn 0.36 log points less than formal entrants. The shift toward formal jobs with experience therefore steepens the national profile:
- **composition term:** +0.038 log points;
- **within term** (flatter informal profiles): −0.035.

The two nearly cancel, and the national height (0.228 log points) is almost the same as the formal one (0.226). P29 is rejected: the flatness of Mexico's profile is a property of formal jobs as much as of the economy as a whole.

### 4.4 Formal profiles have flattened

Estimating the same model separately for four periods (an analysis not in the plan) gives:

| Period | All | Formal | Informal |
|---|---|---|---|
| 2005–2009 | 32.5% | 35.6% | 15.4% |
| 2010–2014 | 28.4% | 28.6% | 17.3% |
| 2015–2019 | 21.6% | 21.0% | 14.7% |
| 2020–2025 | 21.7% | 18.6% | 15.0% |

**Timing.** The formal profile lost about half of its height. Most of the change happened before 2019, so it is not mainly a result of the large increases in the minimum wage from 2019, which raised entry wages.

**Non-response.** Earnings reporting fell over the same years at every level of experience: from 0.90 to 0.74 at 0–4 years and from 0.88 to 0.71 at 20–24 years. A change in who reports could still produce part of the flattening if the experienced formal workers who stopped reporting were the higher earners. ENOE's income ranges, or administrative wage records, would allow a test.

## 5. Robustness and limits

**Cohort adjustment.** The HLT restriction gives negative heights: −26% for all baseline workers, −37% for formal and +6% for informal. With the flat spot at 35–39 years the figures are more negative still.

The same happens on 2005–2018 alone, so the minimum-wage increases are not the cause. The restriction requires that earnings no longer change with experience late in the career and that time effects are common to all workers. In Mexico, cross-sectional earnings fall after 30 years of experience, and the relative wages of older, less-schooled workers changed over the period. Under those conditions the restriction misattributes economy-wide changes to experience. We do not use these estimates. Cohort effects therefore remain a possible source of bias in the cross-sectional profiles. If younger cohorts earn more at a given experience, the cross-section understates true profiles. The flattening across periods, however, compares the same experience bins at different dates.

**Within-person growth.** It avoids cohort effects but is too imprecise to be informative. With one rotation group in each of two windows (about 2,000 formal and 1,000 informal stayers per window), the 90% interval for the implied height runs from about −55% to more than +300%.

**Age heaping.** Removing ages ending in 0 or 5 leaves the baseline height at 26.5%.

## 6. Conclusions

Flat experience–earnings profiles are a general feature of Mexican wage jobs, not a feature of informal ones. On the margin that labour-force surveys observe, formality does not identify jobs that build skills. Sector does somewhat better, with professional, financial and social services and, to a lesser extent, commerce and manufacturing steeper than agriculture and construction. Firm size may matter as well. The steepest profiles in Mexico are still far below rich-country averages.

**For WP09 and the search for motor jobs.** The job characteristics most often used in policy, such as formality and sector, are weak markers of where learning happens. The formal sector has also become flatter over two decades, which suggests that formal employment, as it has grown, has not offered more learning.

**What would change these conclusions:**
- profiles by occupation or by employer, which ENOE does not identify;
- a credible cohort adjustment;
- evidence that the decline in earnings reporting is concentrated among high earners.

## Annex A. Notes on implementation and further work

**A.1 Deviations from the pre-analysis plan.** All were made before estimates were examined unless noted.
- **Birth cohorts.** Single birth years were used instead of five-year groups in the HLT restriction. On synthetic data, five-year groups did not recover a known profile, because a cohort trend within each group loads onto the time effects. Single years did (`tests/test_enoe_profiles.py`).
- **Within-person time effects.** Removed with the growth of flat-spot workers in the same panel, instead of a consumer-price deflator.
- **Coding error.** An error that dropped the year dummies was found by the same tests, and the first run of the estimates was discarded without inspection.
- **Analyses added after seeing the results** (decision D-051):
  - profiles by period;
  - HLT on 2005–2018, to test whether the minimum-wage increases explain the HLT result;
  - earnings reporting by experience and period.

**A.2 Rules applied.** The difference in earnings reporting between formal and informal workers within an experience bin (12.4 points) was below the 15-point threshold that would have required reweighting for non-response.

**A.3 Further work:**
- **Within-person profiles over all windows.** Use all five-quarter windows from 2005 onward, which would raise the within-person sample about twentyfold.
- **Non-response.** Use INEGI's income ranges (`ingocup` brackets) to bound the effect of non-response on the flattening.
- **Other countries' panels** to place Mexico among peers: Brazil's PNAD Contínua, Argentina's EPH, Chile's ENE.
- **Administrative wage records.** Link to administrative records (IMSS) for formal workers, which would give employer identifiers and exact earnings.

## References

- Abel, M., Carranza, E., Geronimo, K. and Ortega, M.E. (2022). Can temporary wage incentives increase formal employment? Experimental evidence from Mexico. IZA Discussion Paper 15740. [L149]
- Lagakos, D., Moll, B., Porzio, T., Qian, N. and Schoellman, T. (2018). Life cycle wage growth across countries. *Journal of Political Economy* 126(2): 797–849. [L148]
