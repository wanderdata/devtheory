# Study 9.8 — Minimum-wage increases of 2019–2024: employment, formality, wages and productivity by state and activity

*Paul Wander. Pre-analysis plan v0.1, 2026-11-16. Written before any outcome was computed for this study. One feasibility check was run before writing: the distribution of the treatment variable (the 2018 bite) across state × activity cells, from ENOE 2018 (Section 2). No outcome after 2018 was examined for this purpose, although study 9.7 has already reported productivity changes between 2017–2019 and 2022–2024 by state, which the author has seen.*

## 1. Question and propositions

Mexico's general minimum wage rose from 88.36 pesos a day in 2018 to 102.68 in 2019, 123.22 in 2020, 141.70 in 2021, 172.87 in 2022, 207.44 in 2023 and 248.93 in 2024, a nominal increase of 182%. In the municipalities of the northern border zone it rose to 176.72 in 2019 and 374.89 in 2024. Study 9.4 examined the 2019 border increase. This study uses the national increases, whose bite differed widely across states and activities, to estimate how employment, formality, wages and value added per worker responded in more exposed cells relative to less exposed ones. The ENOE–PIBE panel of study 9.7 makes it possible to observe output and workers in the same cells.

The design is a difference-in-differences with continuous treatment intensity (Card 1992). Treatment is the bite of the increases in a state × activity cell in 2018, measured before the first increase was announced (December 2018). The estimand is the effect of a higher bite on the change in an outcome relative to cells in the same state and year and in the same activity and year. The identifying assumption is that, in the absence of the increases, outcomes in cells with higher and lower bites would have evolved in parallel after removing state × year and activity × year effects. The estimates are relative effects: workers or output displaced from high-bite cells to low-bite cells in the same state count as a loss in the first and a gain in the second, so the estimates do not measure aggregate effects.

A first-stage check precedes the propositions: the mean log hourly wage of wage employees must rise more in cells with a higher bite (coefficient positive with a 90% interval excluding zero). If it does not, all propositions are reported as inconclusive. Four propositions are tested, each with the post-period estimand of Section 3 (the average of the 2022, 2023 and 2024 coefficients), per unit of bite (a bite of 1 means that every full-time wage employee earned less than the 2019 minimum in 2018), with $\hat\beta_W$ the first-stage coefficient.

P44. A higher bite reduced employment. Outcome: log employed persons aged 15+ in the cell. Supported if the coefficient is negative with a 90% interval excluding zero; rejected if the lower end of the interval is above $-0.3\,\hat\beta_W$, that is, if the data rule out an employment elasticity with respect to the cell's wage more negative than −0.3; inconclusive otherwise.

P45. A higher bite reduced the formal share of employment. Outcome: share of the cell's employed persons in formal employment. Supported if the coefficient is negative with a 90% interval excluding zero; rejected if the lower end of the interval is above −0.10 (ruling out a fall of more than 1 percentage point in the formal share for each 10 points of bite); inconclusive otherwise.

P46. A higher bite raised value added per worker. Outcome: log PIBE value added (constant 2018 prices) per employed person in the cell. Supported if the coefficient is positive with a 90% interval excluding zero; rejected if the upper end of the interval is below $0.25\,\hat\beta_W$ (ruling out productivity gains of a quarter or more of the wage increase); inconclusive otherwise.

P47. A higher bite raised the wages of informal wage employees. Outcome: mean log hourly wage of informal wage employees in the cell. Supported if the coefficient is positive with a 90% interval excluding zero; rejected if the upper end of the interval is below $0.25\,\hat\beta_W$; inconclusive otherwise.

Pre-trend rule. For each outcome the coefficients for 2015, 2016 and 2017 (relative to 2018) are tested jointly with the restricted wild cluster bootstrap. If the p-value is below 0.10, the proposition on that outcome is reported as inconclusive and its estimate as descriptive; an estimate adjusted for a cell-specific linear trend fitted on 2015–2018 is reported alongside, without a decision rule.

## 2. Data

The panel is that of study 9.7: ENOE quarters of 2015–2024 (2020Q2 was not collected; the annual value for 2020 averages the other three quarters) and PIBE value added at constant 2018 prices, by state (Mexico City and the State of Mexico combined, 31 units) and the 20 activity groups, excluding oil. ENOE extracts for 2020–2021, not used in study 9.7, are added.

Bite. For each cell, the bite is the weighted share of full-time wage employees (subordinate and paid workers, 35 or more hours a week) with positive reported monthly income in the main job whose income in 2018 was below 30.4 times the daily minimum that applied to them in 2019 (102.68 pesos, or 176.72 in the border-zone municipalities of study 9.4). The minimum was 88.36 throughout 2018, so the bite is the share of workers that the first increase would have reached at unchanged wages. In the feasibility check, the national bite was 12.8%; 479 of 619 cells had at least 100 such workers in 2018, and across those cells the bite had a median of 7.8%, an interquartile range of 3.7% to 15.9% and a maximum of 72%. By activity the median ranged from 2% (machinery and transport equipment) to 20% (arts, recreation and other services); by state from 2% (Nuevo León) to 33% (Tamaulipas, where the border zone accounts for most of the bite).

Main sample: cells with at least 100 full-time wage employees with reported income in 2018.

Outcomes, annual, 2015–2024:
- W: mean log hourly wage (monthly income divided by 4.33 times weekly hours) of wage employees with positive income and hours, with the non-response weighting classes of study 9.7; W_I the same for informal wage employees;
- E: log employed persons aged 15+;
- F: formal share of employment;
- V: log value added per employed person.

Descriptive outcomes, without propositions: share of full-time wage employees below the current year's minimum; log hours per worker; log value added; the 10th and 50th percentiles of the log hourly wage.

## 3. Estimation

For cell $c$ in state $s$ and activity $a$, and year $t$:

$$y_{ct} = \alpha_c + \delta_{st} + \gamma_{at} + \sum_{k \neq 2018} \beta_k \, \text{bite}_c \, 1[t=k] + \varepsilon_{ct},$$

weighted by the cell's 2018 employment. The post-period estimand is $\bar\beta_{post} = (\beta_{2022} + \beta_{2023} + \beta_{2024})/3$; $\beta_{2019}$ is reported as the first-round effect. The pandemic years 2020 and 2021 are shown but excluded from the estimand. State × year effects absorb state-level shocks, including the change of ENOE's weighting basis in 2020 (which rescales state totals) and state-level pandemic shocks; activity × year effects absorb national activity-specific shocks such as the pandemic's effect on accommodation and food.

Inference: standard errors clustered by state (31 clusters), with 90% intervals from inversion of the restricted wild cluster bootstrap (Rademacher weights), using the routines of study 9.4. Value added is treated as fixed; ENOE's sampling error enters through the cell-level residuals.

## 4. Robustness

- Bite measured in 2017, as the share below 1.162 times the prevailing minimum (the ratio of the 2019 to the 2018 minimum).
- Kaitz index: the 2018 minimum relative to the cell's median monthly income of full-time wage employees.
- Bite among formal wage employees only.
- Cells with at least 50 workers; unweighted.
- Excluding agriculture; accommodation and food; professional, corporate and support services (affected by the 2021 ban on labour subcontracting); government.
- Excluding the southeastern states with large federal projects in 2019–2024 (Campeche, Chiapas, Quintana Roo, Tabasco, Yucatán), and excluding the six border states.
- Clustering by activity group; two-way clustering by state and activity (CR1).
- Linear pre-trend adjustment for every outcome.

## 5. What would change the conclusions

The main threat is shocks specific to a state and activity, correlated with the bite and occurring in the same years. The pandemic is the obvious candidate, since low-wage service cells were hit harder; national activity-level effects are absorbed, but regional differences in the pandemic within an activity are not. The exclusion of 2020–2021 from the estimand and the robustness checks address part of this. Mean reversion is a second threat for the wage outcome: cells with low wages in 2018 because of transitory shocks would show faster wage growth afterwards; the pre-trend test and the 2017 bite address it. Third, workers who move from high-bite to low-bite cells in the same state make relative employment effects larger than aggregate ones. Fourth, ENOE's earnings non-response rose over the period and was higher among formal workers (study 9.2); the weighting classes adjust for observed characteristics only.

## 6. Description

The paper will also report: the event-study coefficients for all outcomes; the implied effect on state aggregate productivity, combining the estimated effects on employment and value added per worker through the decomposition of study 9.7, as an illustration; and the distribution of the bite by state and activity.
