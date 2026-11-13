# Study 9.2 — Which jobs build skills? Experience–earnings profiles by type of job in Mexico

*Paul Wander. Pre-analysis plan v0.1, 2026-11-13. Written before any experience–earnings profile was estimated (D-050). The ENOE files of 2018–19 and 2023–24 had already been used for study 9.1, for flows; no earnings-by-experience tabulation had been made.*

## 1. Question and propositions

Lagakos, Moll, Porzio, Qian and Schoellman (2018, *JPE*; L148) show that wages rise much less with experience in poor countries than in rich ones. For Mexico, on the 1990–2010 censuses, full-time male private-sector wage workers with 20–24 years of potential experience earn 41% more than those with 0–4 years. In rich countries the figure is 89% (their Table 2, p. 806). Their interpretation is that workers in poor countries accumulate less human capital on the job. Their paper does not ask *which* jobs in a poor country have flat profiles.

Two readings are possible:
- **(a) Flatness is general:** every type of job in Mexico has a flat profile.
- **(b) Flatness is concentrated:** some jobs, such as formal jobs, have profiles close to rich-country ones, and the national profile is flat because many workers spend their careers in jobs that teach little.

Reading (b) would identify the jobs that act as "motors" of human-capital accumulation, at the level of the job rather than the sector. Abel, Carranza, Geronimo and Ortega (2022, L149) find, with ENOE, that formal wages of young workers grow much faster than informal ones over 18 months, which points to (b) for early careers.

**P28.** Experience–earnings profiles are much steeper in formal than in informal wage jobs, and differences by formality are larger than differences across sectors.
- **Support:** in both the cross-sectional and the cohort-adjusted estimates (§4), the height at 20–24 years of experience for formal private wage jobs is at least 1.5 times the height for informal ones, and the formal–informal gap exceeds the range of heights across the sector groups of §3.
- **Reject:** the ratio is below 1.2, or the sector range exceeds the formal–informal gap.
- **Inconclusive:** anything in between, or the two estimates disagree.

**P29.** Composition matters: a substantial part of the flatness of Mexico's national profile reflects the type of job workers hold at each level of experience, not only flat profiles within jobs.
- **Support:** in the decomposition of §4.4, the composition term accounts for at least a third of the gap between the national height and the formal-job height.
- **Reject:** it accounts for less than 10%.

## 2. Data

- **Cross-sections:** ENOE first quarters, 2005 to 2025 (21 years). First quarters avoid the 2020 Q2 telephone survey (ETOE) and carry the extended questionnaire.
- **Panels:** the linked windows of study 9.1 (2018 Q4–2019 Q4 and 2023 Q1–2024 Q1) for within-person earnings growth.
- **Baseline sample**, as in Lagakos et al.:
  - men;
  - full-time (35 or more hours a week in the main job);
  - private-sector wage employees (`pos_ocu` = 1, `ambito2` ≠ 7 government);
  - positive hourly earnings;
  - 0–40 years of potential experience.
- **Variants:** women; all hours; own-account workers (`pos_ocu` = 3) as a separate group.
- **Potential experience:** age − 18 for those with fewer than 12 years of schooling, and age − schooling − 6 for those with 12 or more (Lagakos et al., pp. 802–803). Schooling is INEGI's `anios_esc`.
- **Earnings:** INEGI's hourly earnings in the main job (`ing_x_hrs`). Non-response to income questions has grown over the period, so its share is reported by year and type of job (§5).

## 3. Types of job

- **Formality:** formal or informal (`emp_ppal`). This is the main dimension, because formality is reported consistently (study 9.1: 8.7% inconsistency over a year for the same employer).
- **Sector:** six groups, to keep cells large:
  - agriculture and mining;
  - manufacturing;
  - construction;
  - commerce;
  - transport, restaurants and other services;
  - professional, financial and social services.
- **Firm size:** small (up to 10 workers, `ambito2` 2–4) or larger (5–6), reported with the caveat from study 9.1 that size is misreported.

## 4. Estimation

### 4.1 Cross-sectional profiles

Log hourly earnings are regressed on five-year experience bins and year dummies, pooled over 2005–2025, with weights. This is done for all baseline workers and separately for each type of job. The height at bin *b* is exp(coefficient of *b*) − 1 relative to the 0–4 bin. The headline is the height at 20–24 years. Ninety per cent intervals come from a bootstrap over primary sampling units (199 replications).

### 4.2 Cohort-adjusted profiles (Heckman–Lochner–Taber restriction)

Following Lagakos et al. (§IV.B), experience effects are assumed to be zero in the last ten years of the career (30–39 years of experience, the flat spot), with no depreciation. This identifies time effects from the earnings growth of workers in the flat spot. The model has five-year experience bins below 30, one flat-spot group, year dummies and five-year birth-cohort dummies. The variant uses a flat spot of 35–39 years.

**Caveat.** In a country where many older workers move into informal or own-account work, the flat-spot assumption is hard to defend within formal jobs. The cross-sectional and panel estimates are therefore given equal weight.

### 4.3 Within-person growth (synthetic profiles)

From the linked panels of study 9.1, the one-year change in log hourly earnings is computed for men who are full-time private wage employees at both visits and **stay in the same formality status**, by five-year experience bin. Summing average annual growth over the bins gives a synthetic profile for each type of job (Lagakos et al., §V, use panel data for the same purpose). It is free of cohort effects. It conditions on staying in the same type of job, and is noisy because of earnings misreporting. Nominal growth is deflated by the national CPI change over the year; the CPI figures are entered with their source.

### 4.4 Composition decomposition

The national cross-sectional height *H* at 20–24 years is decomposed into:
- the height that would be observed if every worker had the formal profile;
- the effect of informal profiles being flatter;
- the effect of the informal share changing with experience.

The decomposition uses the predicted mean log earnings by bin from §4.1 and the employment shares by bin (an Oaxaca-style split, reported in both orders).

## 5. What would change the conclusions

- **Earnings non-response.** If it differs by more than 15 percentage points between formal and informal workers in the same experience bin, profile comparisons are reported both raw and reweighted on the probability of reporting (age, schooling, sex, state).
- **Selection out of formality.** If informal jobs are disproportionately held by older workers who lost formal jobs, cross-sectional informal profiles are biased downward at high experience. The within-person estimate (§4.3) addresses this. If the two estimates disagree by more than half the cross-sectional gap, the conclusion rests on the within-person estimate.
- **Age heaping** (Lagakos et al. test Mexico for it). Repeated with ages ending in 0 or 5 removed.

## 6. Outputs

Code is in `empirics/code/enoe/profiles/`; aggregate tables go to `empirics/output/enoe/profiles/`; the app page is "9.2 Which jobs build skills?" in `apps/jobs_mexico/`.

## Amendment (before any profile was estimated)

**2026-11-13.** Section 4.3 deflated within-person earnings growth by the national CPI. Instead, economy-wide growth (the time effect) is removed by subtracting the average within-person growth of workers in the flat spot (30–39 years of experience) observed in the same panel and type of job. This is the panel counterpart of the Heckman–Lochner–Taber restriction of §4.2. It needs no external price data and also removes real economy-wide wage growth, which a CPI deflator would leave in. The CPI-deflated version is not computed.

**2026-11-13, before any estimate was examined.** In §4.2, cohorts are single birth years instead of five-year groups. On synthetic data with known experience, time and cohort effects, the five-year version did not recover the experience profile: a cohort trend within each group loads onto the time effects estimated in the flat spot. The single-year version does recover it (`tests/test_enoe_profiles.py`). A coding error that dropped the year dummies was found by the same tests. The first run of the estimates was discarded without inspection.
