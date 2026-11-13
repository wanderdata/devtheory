# WP09 — First results: which jobs are rungs in Mexico?

*Paul Wander. Results note v0.1, 2026-11-13. Design: [`00_pre_analysis_plan.md`](00_pre_analysis_plan.md). Generated tables: [`empirics/output/enoe/results.md`](../../empirics/output/enoe/results.md). Decisions D-046 to D-048.*

## Summary

The pre-analysis plan's test of P-RG3 gives an **inconclusive** result under its own rules, because the two outcomes disagree once spurious transitions are removed.

- **Upward transitions.** Firm size × formality explains more of the variation in upward moves than sector does, in both windows and in every variant. The difference holds for the version the plan requires once misreporting is taken into account: upward moves that involve a change of employer. That version is available only for 2023–24.
- **Exits.** Size × formality also explains more of exits to non-employment in the main sample. But when transitions are required to be confirmed at the next visit, the variant the plan makes decisive in this case, sector and size × formality explain about the same.
- **Manufacturing versus services.** Within the same size × formality cell, manufacturing jobs lead more often to better-paid cells than service jobs do, but they do not have lower exit rates. The plan's second rejection condition, which requires both, is not met.
- **How much the cells explain.** Very little either way. Sector and size × formality together account for 1–7% of the individual variation in these one-year outcomes. Most of what happens to a worker in a year is not predicted by where their job sits on either dimension.

## Data and linking

**Sample.** ENOE, two five-quarter windows: 2018Q4–2019Q4 and 2023Q1–2024Q1. Ages 16–65; complete interviews by usual or new residents.

**Linking.** Of people who were not in their fifth visit:
- **2018–19:** 91–93% are linked to the next quarter.
- **2023–24:** 88–90% are linked.

No link was rejected for a change of sex or an implausible change of age, except one in 2023Q4.

**Person key in 2023–24.** Linking those files required adding TIPO to the person key (D-047). Without it, 10–13% of keys in each quarter belonged to two households.

**Benchmark flows.** Quarterly flows in the self-represented cities, the closest match to Donovan, Lu and Schoellman's urban benchmark, are:
- employment exit: 0.117 (2018–19) and 0.108 (2023–24);
- job finding: 0.21;
- job-to-job moves among employees: 0.045–0.046.

Job-to-job moves are measured only between a fourth quarter and the following first quarter, because the question on the start date with the current employer is asked only in first quarters. These figures still have to be compared with the paper's Mexican estimates, which cover 1995–2017 (OQ-64).

## Misreporting

Among 2,300 employees who reported the same start date with their employer in 2023Q1 and 2024Q1:
- **34%** reported a different firm-size class;
- **8.7%** reported a different formality status.

Some genuine growth across size boundaries is possible over a year, but 34% is far above the 10% threshold the plan set. So firm size, as reported in ENOE, changes with the respondent more often than with the firm. As the plan requires, the upward-transition outcome was redefined to count only moves that involve a change of employer.

That redefinition is possible only in 2023–24. There, both annual visits are first quarters and carry the start-date question. In 2018–19 the annual comparison runs from Q4 to Q4, which has no start-date question.

## The test of P-RG3

Shapley shares of R² are shown with the difference (size × formality minus sector) and its 90% bootstrap interval over primary sampling units.

| Outcome | Window | Main | Confirmed transitions | Self-reports only |
|---|---|---|---|---|
| Exit within a year | 2018–19 | +0.014 [+0.010, +0.019] | −0.004 [−0.015, +0.010] | +0.030 [+0.020, +0.039] |
| Exit within a year | 2023–24 | +0.009 [+0.005, +0.014] | +0.000 [−0.008, +0.007] | +0.029 [+0.020, +0.038] |
| Upward, any | 2018–19 | +0.035 [+0.027, +0.042] | +0.024 [+0.010, +0.042] | +0.047 [+0.034, +0.061] |
| Upward, any | 2023–24 | +0.043 [+0.035, +0.052] | +0.039 [+0.022, +0.072] | +0.047 [+0.033, +0.060] |
| Upward, with a change of employer | 2023–24 | +0.005 [+0.003, +0.009] | +0.005 [+0.000, +0.011] | +0.005 [−0.000, +0.012] |

**Exits.** Requiring a transition to be confirmed at the next visit removes the advantage of size × formality. The confirmed sample is much smaller, about 6,700 against 25,000, because it keeps only people whose state at the first and last visits is repeated at the adjacent visit. In that sample the two dimensions explain about the same share of exits.

**Upward transitions, any.** This version has a ceiling. Cells already near the top of the earnings ranking can hardly move up, and size × formality tracks earnings more closely than sector does. An exploratory variant, not in the plan (D-048), conditions on the origin cell's earnings-rank decile. It reduces the difference to +0.029 (2018–19) and +0.015 (2023–24), and both intervals still exclude zero.

**Upward transitions with a change of employer.** This is the version the plan requires once misreporting exceeds 10%. Size × formality still explains more, although both shares are small (0.009 against 0.004).

## Manufacturing versus services within size × formality cells

The effect of a manufacturing rather than a service job (rama_est2 5–10) is estimated with controls for size × formality, age group, sex and schooling level.

| Outcome | Window | Services mean | Manufacturing − services [90%] |
|---|---|---|---|
| Exit within a year | 2018–19 | 0.157 | +0.022 [+0.000, +0.044] |
| Exit within a year | 2023–24 | 0.146 | +0.017 [−0.001, +0.034] |
| Upward, any | 2018–19 | 0.248 | +0.049 [+0.023, +0.075] |
| Upward, any | 2023–24 | 0.237 | +0.092 [+0.068, +0.117] |
| Upward, with a change of employer | 2023–24 | 0.040 | +0.014 [+0.002, +0.025] |

In the same size × formality cell, a manufacturing job is somewhat more likely than a service job to lead to a better-paid cell within a year, including through a change of employer (+1.4 points on a base of 4.0). It is not less likely to end in non-employment; the point estimates are slightly higher. On the job-ladder mechanism, manufacturing therefore offers better upward mobility but not more stability. That is consistent with the WP07 finding that manufacturing's employment share, rather than its output share, is associated with growth. It is also consistent with manufacturing jobs being where workers move up from.

## What this does and does not show

- **Descriptive only.** These are not causal effects of holding a job. People who get formal jobs in large firms differ from those who do not, in ways the controls only partly capture.
- **Low explained variance.** A share of 1–7% means the cells summarise little of what happens to individuals. The comparison between dimensions is about which summary is less poor.
- **Firm size is badly measured.** In ENOE it is reported with a lot of error, which weakens any result that depends on it. Formality is reported much more consistently (8.7% inconsistency over a year).
- **One-year horizon.** The analysis follows people for at most a year. A job ladder can work over longer spans, which ENOE's rotation cannot follow.

## Next steps

1. **Compare the benchmark flows** with Donovan, Lu and Schoellman's Mexican figures (OQ-64).
2. **Formality alone.** Repeat the test with formality alone against sector, since formality is reported reliably and size is not.
3. **Feed the job-cell results into WP08's ladder for Mexico** (P26). The cells provide the steps within sectors that the sector-level ladder lacks. Productivity by cell would come from INEGI's informal-economy accounts.
