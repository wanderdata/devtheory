# Experience–Earnings Profiles by Type of Job in Mexico, 2005–2025

*Paul Wander. Working draft v0.2, 2026-11-16. Pre-analysis plan: [`00_pre_analysis_plan.md`](00_pre_analysis_plan.md). Generated tables: [`empirics/output/enoe/profiles/results.md`](../../../empirics/output/enoe/profiles/results.md). App: Jobs in Mexico, page 9.2.*

## Abstract

Hourly earnings rise much less with potential experience in poor countries than in rich ones. Using 21 first-quarter cross-sections of Mexico's labour-force survey (ENOE), 2005–2025, and the sample definition of Lagakos et al. (2018), this paper estimates experience–earnings profiles by formality, sector and establishment size. Among full-time male private-sector wage employees (859,695 observations), hourly earnings at 20–24 years of potential experience are 25.7% above those at 0–4 years (90% interval 24.9–26.4%); 25.4% for formal and 15.6% for informal jobs. The height ranges across six sectors from 14.6% to 35.6%, more than the difference by formality, and in manufacturing and commerce, the two sectors with enough informal wage employees for separate estimates, formal and informal profiles are similar. The formal profile flattened from 35.6% in 2005–2009 to 18.6% in 2020–2025. Reweighting for earnings non-response raises the heights by between 0.6 and 5.6 points without changing these comparisons. The cohort correction of Heckman, Lochner and Taber produces negative heights in these data and is not used.

## 1. Introduction

Lagakos, Moll, Porzio, Qian and Schoellman (2018) show that experience–wage profiles are about twice as steep in rich countries as in poor ones; on Mexican census data for 1990–2010 they estimate wages at 20–24 years of potential experience to be 41% above those of entrants, against about 89% on average in the rich countries of their sample. The finding is read as evidence that workers in poor countries accumulate less human capital over their careers. It leaves open which jobs, if any, offer the learning that most jobs in a poor country do not.

The question matters for this programme, which looks for the jobs that carry productivity growth. If formal jobs, or jobs in particular sectors, have markedly steeper profiles, they would be candidates for the jobs through which skills accumulate. Two propositions were stated before estimation: that profiles are much steeper in formal than in informal jobs, with a formality gap larger than differences across sectors (P28); and that much of the flatness of the national profile reflects the type of job workers hold at different stages of their careers (P29).

## 2. Data

The paper uses the first quarter of each year from 2005 to 2025. The baseline sample follows Lagakos et al.: men working full time (35 hours a week or more) as private-sector wage employees, with 0–40 years of potential experience, defined as age minus 18 for those with fewer than 12 years of schooling and age minus schooling minus 6 otherwise. Estimates use those with positive hourly earnings (859,695 observations). Formality follows INEGI's labour-informality definition. Sectors are six groups formed from INEGI's eleven. Establishment size has two classes, micro and small against medium and large establishments, using INEGI's sector-specific thresholds (micro means up to 15 workers in industry and up to 5 in commerce and services); study 9.1 found size to be reported with substantial error.

The share of baseline workers reporting positive hourly earnings, computed before the positive-earnings restriction, fell over the period from 90% to 57% among formal workers and from 93% to 70% among informal ones. Pooled over all years, the formal–informal difference in reporting within an experience bin is at most 12.4 points. By year and experience bin, it exceeds 15 points in 12 of 168 cells (at most 17.6 points, in 2018 at 20–24 years), always with lower reporting among formal workers.

## 3. Estimation

Log hourly earnings are regressed on indicators for five-year experience bins and for years, pooled over 2005–2025 with survey weights. The height of a profile at bin *b* is the exponential of its coefficient minus one, relative to the 0–4 bin; the paper reports heights at 20–24 years. Intervals come from a bootstrap that resamples primary sampling units within state and year (199 replications).

Cross-sectional profiles mix experience effects with differences between birth cohorts. Lagakos et al. separate them with the Heckman–Lochner–Taber (HLT) restriction that earnings do not grow with experience late in the career, so that wage growth of late-career workers identifies time effects. The restriction is applied here with single-year birth cohorts.

As a check on cohort effects and on selection out of formal jobs, one-year earnings growth of workers who stay in the same type of job is computed from the linked panels of study 9.1, net of the growth of workers with 30–39 years of experience in the same type of job.

Mean log earnings imply an exact decomposition of the difference between the national and the formal profile heights. With informal shares s₀ and s₂₀ at 0–4 and 20–24 years, heights c_F and c_I in logs, and an informal–formal earnings gap at entry g₀:

national height − formal height = s₂₀(c_I − c_F) + (s₂₀ − s₀)g₀.

The first term is the contribution of flatter informal profiles and the second that of the change in the informal share with experience. The decomposition can also be taken in the other order (weighting the profile difference by s₀ and the change in shares by the gap at 20–24 years); both are reported. Because the heights are year-adjusted regression coefficients, the identity holds only approximately.

To meet the non-response rule of the plan (§5), profiles are also estimated with survey weights divided by the fitted probability of reporting earnings from a logit on year × formality, five-year age groups, single years of schooling and state; this analysis was carried out after the independent audit of the programme found the rule triggered by year and bin (D-064).

## 4. Results

### 4.1 Heights by type of job

*Table 1. Height of the experience–earnings profile at 20–24 years relative to 0–4 years*

| Group | Height | 90% interval | Observations |
|---|---|---|---|
| All baseline workers | 25.7% | 24.9–26.4% | 859,695 |
| Formal | 25.4% | 24.5–26.4% | 506,847 |
| Informal | 15.6% | 14.8–16.4% | 352,848 |
| Medium and large establishments | 30.6% | 29.1–32.0% | 295,855 |
| Micro and small establishments | 24.6% | 23.7–25.6% | 436,777 |
| Women (otherwise baseline) | 16.8% | 15.9–17.6% | 469,198 |
| Own-account men, all hours | −9.4% | −12.1 to −7.0% | 227,334 |

The national height of 26% is below the 41% that Lagakos et al. estimate for Mexico on census data for 1990–2010; part of the difference may come from the source and part from the flattening described in Section 4.4. Profiles peak at 20–29 years and decline afterwards, with the baseline height at 16% at 35–39 years. Formal earnings at 20–24 years are a quarter above those at entry, less than a third of the rich-country average in Lagakos et al. Earnings of own-account workers fall with experience.

### 4.2 Sector and formality

*Table 2. Height at 20–24 years by sector, and by formality within two sectors*

| Sector | All | Formal | Informal |
|---|---|---|---|
| Professional, financial and social services | 35.6% | | |
| Commerce | 29.4% | 24.0% | 23.3% |
| Manufacturing | 27.9% | 22.7% | 22.9% |
| Transport, restaurants and other services | 24.1% | | |
| Construction | 21.4% | | |
| Agriculture and mining | 14.6% | | |

The range of heights across sectors (21 points) is larger than the difference between pooled formal and informal profiles (9.8 points). In manufacturing and commerce, the only sectors with enough informal wage employees for separate estimates, formal and informal profiles are similar. In those two sectors at least, the pooled formality gap reflects the sectors in which formal and informal jobs are found; whether this holds in the other sectors cannot be established with these data. Profiles are steeper in medium and large establishments (31%) than in micro and small ones (25%), subject to the reporting error in establishment size.

### 4.3 Composition

At 0–4 years of experience, 54.3% of baseline workers are informal; at 20–24 years, 43.7%. Informal entrants earn 0.357 log points less than formal entrants. In the first ordering of the decomposition, flatter informal profiles lower the national height by 0.035 log points and the shift towards formal jobs with experience raises it by 0.038; in the second ordering the terms are −0.044 and 0.046. In both, the two effects nearly cancel, and the national height (0.228 log points) is almost equal to the formal height (0.226). The flatness of the national profile is therefore a property of formal jobs as much as of the economy as a whole.

### 4.4 Change over time

*Table 3. Height at 20–24 years by period (estimated separately; an analysis not in the plan)*

| Period | All | Formal | Informal |
|---|---|---|---|
| 2005–2009 | 32.5% | 35.6% | 15.4% |
| 2010–2014 | 28.4% | 28.6% | 17.3% |
| 2015–2019 | 21.6% | 21.0% | 14.7% |
| 2020–2025 | 21.7% | 18.6% | 15.0% |

The formal profile lost about half of its height, mostly before 2019, so the change is not mainly a result of the large increases in the minimum wage from 2019, which raised entry wages. Earnings reporting fell over the same years at every level of experience, from 0.90 to 0.74 at 0–4 years and from 0.88 to 0.71 at 20–24 years. A change in who reports could contribute to the flattening if the experienced formal workers who stopped reporting were higher earners.

### 4.5 Reweighting for non-response

*Table 4. Height at 20–24 years, raw and reweighted for earnings non-response*

| Group | Raw | Reweighted | 90% interval, reweighted |
|---|---|---|---|
| All baseline workers | 25.7% | 28.6% | 27.6–29.5% |
| Formal | 25.4% | 28.1% | 26.6–29.8% |
| Informal | 15.6% | 16.6% | 15.8–17.4% |

Reweighting raises all heights, by 1.0 point for informal, 2.8 for formal and between 0.6 and 5.6 points across sectors (from 16.1% in agriculture and mining to 41.2% in professional, financial and social services). The formal–informal difference becomes 11.5 points, still smaller than the sector range of 25 points, and in the composition decomposition the two terms again nearly cancel (−0.038 and 0.044 log points in the first ordering).

### 4.6 Propositions

P28 is rejected on the cross-sectional evidence: the range across sectors exceeds the formality gap, raw and reweighted, and the HLT estimates give a negative formal–informal ratio. The plan's §5 also states that if within-person estimates disagree with the cross-section by more than half the cross-sectional gap, the conclusion rests on the within-person estimates. They do disagree (formal minus informal implied heights of 0.19 and −1.18, against a cross-sectional gap of 0.098), but their 90% intervals run from about −50% to between 280% and 1,090% (Section 5), so that resting the conclusion on them would leave P28 undetermined. The verdict is reported as rejected on the cross-section and undetermined under the within-person rule.

P29 is recorded as rejected, which departs from the plan's rule as written (D-064). The rule supports P29 if the composition term is at least a third of the gap between the national and the formal height. The gap is 0.002 log points and the composition term 0.038, so the rule read literally gives support. The rule presumed a national profile flatter than the formal one; here the two are equal, and composition steepens rather than flattens the national profile, which is the opposite of what P29 asserts.

## 5. Limitations

The HLT restriction gives negative heights: −26% for all baseline workers, −37% for formal and 6% for informal, and more negative with the flat spot at 35–39 years. The same happens on 2005–2018 alone, so the minimum-wage increases are not the cause. The restriction requires that earnings no longer change with experience late in the career and that time effects are common to all workers; in Mexico, cross-sectional earnings fall after 30 years of experience and the relative wages of older, less-schooled workers changed over the period. Under these conditions the restriction attributes economy-wide changes to experience, and its estimates are not used. Cohort effects therefore remain a possible source of bias in the cross-sectional profiles: if younger cohorts earn more at given experience, the cross-section understates true profiles. The comparison across periods in Section 4.4, which compares the same experience bins at different dates, is less affected.

Within-person growth avoids cohort effects but is too imprecise to be informative. With one rotation group in each of two windows (about 2,000 formal and 1,000 informal stayers per window), the 90% intervals of the implied heights have lower bounds between −44% and −70% and upper bounds between 280% and 1,090%.

Removing ages ending in 0 or 5 leaves the baseline height at 26.5%.

## 6. Conclusions

Flat experience–earnings profiles are a general feature of Mexican wage employment and not a particular feature of informal jobs. In the two sectors where the comparison is possible, formal and informal profiles are similar, and differences across sectors are larger than differences by formality. Formal profiles have become flatter over two decades, from about 36% to 19% at 20–24 years, so the growth of formal employment has not been accompanied by steeper earnings growth with experience. These conclusions hold when the profiles are reweighted for earnings non-response. Profiles by occupation or employer, which ENOE does not record, a credible correction for cohort effects, and evidence on whether non-reporting is concentrated among high earners would test them further.

## Annex A. Implementation notes and further work

Deviations from the plan made before estimates were examined: single birth years instead of five-year groups in the HLT restriction (with five-year groups a cohort trend within each group loads onto the time effects, and synthetic tests did not recover a known profile; single years did); and removal of time effects in the within-person estimates with the growth of flat-spot workers in the same panel instead of a consumer-price deflator. A coding error that dropped the year indicators was found by the same tests, and the first run of estimates was discarded without inspection.

Analyses added after results were seen (D-051): profiles by period, HLT on 2005–2018, and earnings reporting by experience and period. Added after the independent audit (D-064): reweighting for non-response, the year-by-bin check of the non-response rule and the second ordering of the composition decomposition.

Further work could use all five-quarter windows from 2005 onward for within-person profiles, raising the sample about twentyfold; use INEGI's income ranges to bound the effect of non-response on the flattening; place Mexico among peers with Brazil's PNAD Contínua, Argentina's EPH and Chile's ENE; and link formal workers to IMSS records for employer identifiers and exact earnings.

## References

Lagakos, D., Moll, B., Porzio, T., Qian, N. and Schoellman, T. (2018). Life cycle wage growth across countries. *Journal of Political Economy* 126(2): 797–849. [L148]
