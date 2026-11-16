# Minimum-Wage Increases of 2019–2024 in Mexico: Wages, Employment, Formality and Value Added by State and Activity

*Paul Wander. Working draft v0.1, 2026-11-16. Pre-analysis plan: [`00_pre_analysis_plan.md`](00_pre_analysis_plan.md). Generated tables: [`empirics/output/enoe/minimum_wage_bite/results.md`](../../../empirics/output/enoe/minimum_wage_bite/results.md). App: Jobs in Mexico, page 9.8.*

## Abstract

Mexico's general minimum wage rose from 88.36 pesos a day in 2018 to 248.93 in 2024. This paper compares 479 state × activity cells according to the share of their full-time wage employees who earned less than the 2019 minimum in 2018 (the bite: median 7.8%, interquartile range 3.7% to 15.9%). It combines the labour-force survey (ENOE) with value added from INEGI's state accounts (PIBE), and uses a difference-in-differences design with cell, state × year and activity × year effects. Averaged over 2022–2024 and relative to 2018, ten additional points of bite are associated with hourly wages of wage employees 3.4% higher (90% interval 2.5% to 4.4%), with a formal share of employment 0.5 points higher (0.2 to 0.7), and with value added per worker 1.6% higher (0.0% to 2.8%). The estimates for employment, −1.5% (−3.6% to 0.7%), and for value added, 0.0% (−1.7% to 2.0%), are imprecise. Value added per worker therefore rose because measured employment fell, not because output grew, and the result depends on agriculture. Wages of informal wage employees rose by 2.6% (1.5% to 3.7%), but their pre-trend test fails at the 10% level. Coefficients before 2018 indicate that measuring the bite and the base-year outcomes in the same sample produces mean reversion; with the bite measured in 2017, the wage and formality results are smaller but similar in direction, and the pre-trend tests pass. The estimates are relative effects between cells and do not measure the aggregate effect of the increases.

## 1. Introduction

Studies 9.1–9.7 of this programme are descriptive. This study uses a large policy change to estimate effects. Between 2018 and 2024 Mexico's general minimum wage rose by 182% in nominal terms, and by much more than prices, after decades in which it had fallen far below most wages. Study 9.4 examined the 2019 doubling in the northern border zone. The national increases affected every state, but they reached a larger share of workers in states and activities where pay was low. That difference in exposure is the source of identification here, following Card (1992).

The panel built in study 9.7 contributes value added per worker. A minimum-wage increase could raise measured productivity in three ways: by raising effort or investment within firms, by moving workers towards more productive firms (Dustmann et al. 2022), or by reducing employment while output stays constant. The data can distinguish the last of these from the first two. The paper tests four propositions set out in a pre-analysis plan before any outcome was computed.

## 2. Data and treatment

Cells are defined by state (Mexico City and the State of Mexico combined, 31 units) and the 20 activity groups of study 9.7, excluding oil. ENOE provides employment, formality, hours and labour income for every quarter of 2015–2024 (2020Q2 was not collected), and PIBE gives value added at constant 2018 prices.

The bite of a cell is the weighted share of full-time wage employees (35 or more hours a week) with positive reported income whose monthly income in 2018 was below 30.4 times the daily minimum that applied to them in 2019: 102.68 pesos, or 176.72 in the 43 municipalities of the northern border zone. The minimum was 88.36 throughout 2018, so the bite is the share of workers the first increase would reach at unchanged pay. The sample comprises the 479 of 619 cells with at least 100 such workers in 2018, which account for 98% of employment. The national bite was 12.8%. Weighted by employment, it was highest in agriculture (31%) and in arts, recreation and other services, retail, and machinery and transport equipment (17% to 19%, the last because of the border states). Across cells it has a correlation of 0.93 with the bite measured in 2017 and of 0.69 with the Kaitz index.

Outcomes are annual: mean log hourly wage of wage employees (with weighting classes for earnings non-response, as in study 9.7); the same for formal and for informal wage employees; log employed persons aged 15 and over; formal share of employment; and log value added per employed person.

## 3. Method

For cell $c$ in state $s$, activity $a$ and year $t$, the estimated equation is

$$y_{ct} = \alpha_c + \delta_{st} + \gamma_{at} + \sum_{k \neq 2018} \beta_k\,\text{bite}_c\,1[t=k] + \varepsilon_{ct},$$

weighted by 2018 employment, with standard errors clustered by state. The estimand is the mean of the 2022–2024 coefficients. Intervals invert the restricted wild cluster bootstrap with 31 clusters. Effects below are stated for ten points of bite, that is, the coefficients divided by ten. The identifying assumption is that, without the increases, outcomes in cells with higher and lower bites would have followed parallel paths once state × year and activity × year effects are removed. State × year effects absorb state-wide shocks, including the change of ENOE's weighting basis in 2020. Activity × year effects absorb national shocks to an activity, such as the pandemic's effect on restaurants.

## 4. Results

### 4.1 Wages

*Table 1. Effects of ten points of bite, mean of 2022–2024 relative to 2018*

| Outcome | Effect | 90% interval | 2019 | Pre-trend p |
|---|---|---|---|---|
| Mean log hourly wage, wage employees | 0.034 | 0.025 to 0.044 | 0.024 | 0.016 |
| Mean log hourly wage, informal wage employees | 0.026 | 0.015 to 0.037 | 0.017 | 0.080 |
| 10th percentile, log hourly wage | 0.027 | 0.012 to 0.049 | 0.014 | 0.350 |
| Log employment | −0.015 | −0.036 to 0.007 | −0.011 | 0.989 |
| Formal share of employment | 0.005 | 0.002 to 0.007 | 0.004 | 0.253 |
| Log value added per worker | 0.016 | 0.000 to 0.028 | 0.014 | 0.600 |
| Log value added | 0.000 | −0.017 to 0.020 | 0.003 | 0.465 |

*479 cells; intervals from the wild cluster bootstrap; pre-trend p is the joint test of the 2015–2017 coefficients.*

Wages rose more where the bite was larger: by 2.4% for ten points of bite in 2019 and by 3.4% on average in 2022–2024. Because the bite is a share of workers, an effect of 3.4% for ten points corresponds to an increase of about a third in the pay of the workers counted in the bite, if all of it fell on them. The pre-trend test fails (p = 0.016). The coefficients for 2015–2017 are positive (0.013 to 0.016 for ten points), and 2018, the year in which the bite is measured, stands out as low. This is the pattern expected when the bite and the base-year outcome come from the same sample. A cell whose 2018 sample happens to contain more low-paid workers has both a higher bite and lower 2018 wages, and wages in other years revert. With the bite measured in the first three quarters of 2017 (Section 4.4), the pre-trend test passes (p = 0.45) and the wage effect is 3.1% (2.1% to 4.6%) relative to 2018, or 2.3% relative to the mean of 2015–2017.

Wages of informal wage employees, to whom the minimum is rarely enforced, also rose more in high-bite cells: by 2.6% for ten points (1.5% to 3.7%), three quarters of the effect on all wage employees. This is consistent with the minimum acting as a reference for informal pay (Bosch and Manacorda 2010). The pre-trend test gives p = 0.080; with the 2017 bite it gives 0.125, and the effect is 2.1% (0.9% to 3.5%).

### 4.2 Employment and formality

Employment fell by 1.5% for ten points of bite (−3.6% to 0.7%), relative to cells in the same state and activity. That implies an elasticity with respect to the cell's wage of −0.45, but the interval is wide, and the estimate changes with the specification. With the 2017 bite it is −2.3% (−4.5% to 0.9%). Unweighted it is +0.2%. Excluding agriculture it is +2.1%, but there the coefficients for 2015–2017 average +2.9%: non-agricultural high-bite cells were losing employment relative to others before 2018, and the post-2018 coefficient is slightly below that earlier level.

The formal share of employment rose by 0.5 points for ten points of bite (0.2 to 0.7), and by 0.2 points (−0.25 to 0.56) with the 2017 bite. Neither specification shows the fall in formality that a higher minimum could cause by pricing low-paid workers out of formal jobs.

### 4.3 Value added per worker

Value added per worker rose by 1.6% for ten points of bite (0.0% to 2.8%). Value added itself did not change detectably (0.0%, −1.7% to 2.0%), so the rise in value added per worker mirrors the fall in measured employment. The increase does not come from additional output, and nothing in these data shows productivity improving within firms or workers moving to more productive ones. The estimate is also fragile. Excluding agriculture it is −1.9% (−4.7% to 0.5%), with a failing pre-trend test, and with the 2017 bite it is 2.0% (−0.7% to 3.8%). In agriculture the bite was highest and employment has been falling for decades, and this drives the result. As an illustration only, applying the estimates to every cell would imply that the increases raised non-oil productivity by 0.4 to 6.5 log points across states relative to their least-exposed cells, with a median of 2.1. That calculation inherits all the fragility above.

### 4.4 Robustness and diagnostics

The wage, formality and employment results keep their sign across most specifications in the generated tables: the Kaitz index, the bite among formal employees, cells with at least 50 workers, and the exclusion of accommodation and food, of professional and support services (affected by the 2021 ban on subcontracting) or of government. With the bite among formal employees, the employment and productivity estimates change sign. Excluding the southeastern states with large federal projects reduces the employment and productivity estimates to about a quarter and two thirds of the main ones. Removing a cell-specific linear trend fitted on 2015–2018 raises the wage effect to 5.3% and leaves the employment and productivity estimates without precision.

### 4.5 Propositions

Under the decision rules of the plan, P44 (a higher bite reduced employment) is inconclusive: the point estimate is negative, but the interval includes zero and does not rule out an elasticity of −0.3. P45 (a higher bite reduced the formal share) is rejected: the lower end of the interval, +0.019 per unit of bite, is above the threshold of −0.10, and the point estimate is positive. P46 (a higher bite raised value added per worker) is supported, with a lower interval bound of 0.004. The increase reflects lower employment with unchanged value added, and it is not robust to excluding agriculture or to measuring the bite in 2017. P47 (wages of informal wage employees rose) is inconclusive under the pre-trend rule (p = 0.080), although the estimate is positive and its interval excludes zero. The first-stage check is passed, but its own pre-trend test fails, for the reason given in Section 4.1.

## 5. Limitations

The estimates compare cells within the same state and year and within the same activity and year. They measure relative effects. If the increases reduced employment everywhere, or moved workers from high-bite to low-bite cells in the same state, the relative estimates misstate the aggregate effect. In the second case they overstate the fall in high-bite cells.

The pandemic falls in the middle of the period. National effects on activities and state-wide effects are absorbed, but a pandemic effect specific to a state and activity and correlated with the bite is not. The estimand excludes 2020–2021, and the coefficients for 2022–2024 are close to one another.

The bite is measured with sampling error, and in the base year with the same sample as the outcomes. This produces the mean reversion seen in the wage and formality coefficients. The 2017 bite reduces the problem but does not remove it, because ENOE's rotating panel re-interviews some 2017 dwellings in 2018.

Earnings non-response rose over the period and is adjusted only for observed characteristics. Value added comes from PIBE at state level and employment from a household survey, with the measurement problems described in study 9.7.

## 6. Conclusions

Mexico's minimum-wage increases raised pay more where they reached more workers, including the pay of informal wage employees. There is no evidence that they reduced the formal share of employment; if anything it rose. The estimates for employment are negative but imprecise and depend on agriculture. Value added did not respond detectably, so where value added per worker rose it did so through fewer workers, not more output. A wage-push effect on productivity of the kind found for Germany is not visible at the level of states and activities. Firm-level data would be needed to see it, such as the economic census of 2024 or IMSS records, which would show whether workers moved to more productive employers.

## Annex A. Implementation notes and departures from the plan

These are recorded in decisions D-068 and D-069.

1. The diagnostics of Section 4.4 that use the bite measured in 2017 and the exclusion of agriculture, with wild-bootstrap intervals and pre-trend tests (step `03b_diagnostics.py`), were added after the main estimates had been seen, because the event studies showed coefficients for 2015–2017 of the same sign as the post-period ones. The plan listed the 2017 bite and the exclusion of agriculture as robustness checks with CR1 intervals; the decision rules are applied to the main specification only.
2. The fixed-effects routine shared with study 9.4 projected out the fixed effects with a QR decomposition without column pivoting. With three sets of fixed effects and several linear dependencies among them, this gave incorrect coefficients; the error was found with a synthetic-data test written for this study. The routine now uses pivoted QR. In study 9.4 the correction changes only the specification with state × quarter effects (for example, the informal-to-formal transition estimate moves from −1.9 to −2.3 points), which is not cited in that paper beyond its sign; in study 9.5 it changes nothing beyond rounding.
3. The 2015 minimum used for the descriptive share below the current minimum is that of the general area from October 2015 (70.10 pesos).
4. Employment for each cell includes persons whose industry code does not identify an activity, distributed within state and year; wages exclude them.

## References

Bosch, M. and Manacorda, M. (2010). Minimum wages and earnings inequality in urban Mexico. *American Economic Journal: Applied Economics* 2(4): 128–149. [L172]

Card, D. (1992). Using regional variation in wages to measure the effects of the federal minimum wage. *Industrial and Labor Relations Review* 46(1): 22–37. [L170]

Dustmann, C., Lindner, A., Schönberg, U., Umkehrer, M. and vom Berge, P. (2022). Reallocation effects of the minimum wage. *Quarterly Journal of Economics* 137(1): 267–328. [L171]

INEGI (2026). Producto Interno Bruto por Entidad Federativa, base 2018. [L163]

Minimum-wage schedule: CONASAMI resolutions published in the Diario Oficial de la Federación, as compiled in L169.
