# Where Workers Move Up: Job Mobility and Growth across Mexican States, 2005–2025

*Paul Wander. Working draft v0.1, 2026-11-16. Pre-analysis plan: [`00_pre_analysis_plan.md`](00_pre_analysis_plan.md). Generated tables: [`empirics/output/enoe/states/results.md`](../../../empirics/output/enoe/states/results.md). App: Jobs in Mexico, page 9.6.*

## Abstract

We measure, for each of Mexico's 32 states, how often workers move up within a year: from informal to formal employment, or into a better-paid type of job. We use 2.8 million people followed for a year in the national labour-force survey (ENOE), 2005–2025, and adjust for age, sex, schooling, sector and urban residence.

**Differences between states.** The differences are large. The adjusted one-year informal-to-formal rate ranges from 6% in Querétaro to 19% in Guerrero, around a mean of 12% in 2005–2011. Almost all of this variation is real rather than sampling noise.

**Persistence.** The differences also persist: the state ranking in 2005–2011 predicts the ranking in 2012–2018 and 2022–2025 with correlations of 0.96 and 0.97.

**Growth.** States with more informal-to-formal mobility in 2005–2011 grew faster in GDP per person over 2012–2019. The rank correlation is 0.32, with a 90% interval of 0.01 to 0.55, across the 30 states without large oil production. The relation holds conditional on initial income and formal share, and with non-oil GDP for all 32 states. It is weak and rests on 30 observations, and it describes co-movement, not cause.

## 1. Introduction

**From jobs to places.** Studies 9.1–9.5 describe how Mexican workers move between jobs. Those moves take place in local labour markets that differ in industry, firm structure and growth. If some states offer more upward moves to the same kind of worker, mobility is partly a property of places. That raises the question this programme started from, at a lower level of aggregation: do places where workers move up grow faster?

**Earlier evidence.** International comparisons find that poorer countries have more churning and less upward mobility (Donovan, Lu and Schoellman 2023). Within Mexico, the large differences between the north and centre and the south in productivity and growth are well documented. Differences in workers' mobility across states, measured on comparable panels, have received less attention.

**This paper.** It measures mobility by state with ENOE's rotating panel, adjusts it for composition, and tests three propositions stated before estimation:
- **P38:** states differ beyond composition and sampling error;
- **P39:** the differences persist;
- **P40:** states with more mobility grew faster afterwards.

## 2. Data

**Mobility.** ENOE, every quarter from 2005 to 2019 and from 2022 to 2026. Persons aged 16–65 at their first interview are linked to their fifth, one year later; 76% are linked. Panels are grouped by starting year: 2005–2011, 2012–2018 and 2022–2025. Each person is assigned to their state of residence at the first interview.

**Measures**, one year after the first interview:
- **M1:** among the informally employed, the share formally employed.
- **M2:** among the employed, the share in a sector × formality cell with higher national median hourly earnings. Establishment size is left out because it is misreported (study 9.1).
- **M3:** among the employed, the share not employed.

M1 rests on about 370,000 informal workers in each of the first two periods.

**GDP.** INEGI's state accounts (PIBE), base 2018, at constant 2018 prices. The states add up exactly to the national total. INEGI builds state GDP from establishment-level census and survey data, assigning each establishment's value added to the state where it is located. Non-oil GDP subtracts oil-mining value added, which is 74% of Campeche's GDP and 37% of Tabasco's in 2019. Population is taken from ENOE's survey weights, all ages, as an annual average.

## 3. Method

**Adjusted state measures.** For each measure and period, a weighted linear probability model is estimated with:
- fixed effects for each of the 32 states;
- fixed effects for the starting quarter, single years of age, sex, single years of schooling, sector at the first interview, formality (for M2 and M3) and urban residence.

The adjusted measure for a state is its predicted rate at the national average composition. Standard errors are clustered by primary sampling unit.

**Signal and persistence.**
- **Signal:** the variance of true state effects is estimated as the variance of the 32 estimates minus their mean sampling variance.
- **Persistence:** the correlation between periods is corrected for sampling error by dividing by the square root of the product of the two reliabilities.

**Growth.** Spearman's rank correlation between the 2005–2011 measure and growth of GDP per person over 2012–2019 (log points a year). Campeche and Tabasco are excluded from the main test. Intervals come from 1,999 bootstrap resamples of states.

## 4. Results

### 4.1 States differ, and the differences are real

| Measure | Mean | Standard deviation across states | Lowest | Highest |
|---|---|---|---|---|
| M1, informal to formal (2005–2011) | 12.3% | 3.2 | 6.3% (Querétaro) | 19.1% (Guerrero) |
| M2, upward move (2005–2011) | 13.7% | 2.0 | 9.9% | 17.3% |
| M3, exit to non-employment (2005–2011) | 14.1% | 1.4 | 10.5% | 16.9% |

**Signal.** For M1, the variance of the estimated state effects is 50 times the average sampling variance: 98% of it is signal. P38 is supported. The same holds for M2 (96%) and M3 (94%).

**Composition.** Adjustment matters for M2. The variance of upward moves across states is 3.7 times larger after adjustment than before, so differences in workforce composition partly offset differences in mobility between states.

**What M1 is not.** The informal-to-formal rate is unrelated to the state's formal share of employment: the rank correlation is −0.01. Some states with large formal sectors have few moves into them (Querétaro, Coahuila), and some with small formal sectors have many (Guerrero, Puebla, Tlaxcala). M1 measures movement, not the size of the formal sector.

**Urban areas.** Restricting to urban areas gives a ranking that correlates 0.92–0.93 with the main one.

### 4.2 The differences persist

| Measure | 2005–2011 vs 2012–2018 | 2012–2018 vs 2022–2025 |
|---|---|---|
| M1, informal to formal | 0.96 (0.93–0.98) | 0.97 (0.96–0.99) |
| M2, upward move | 0.93 (0.89–0.96) | 0.93 (0.88–0.97) |
| M3, exit | 0.61 (0.26–0.77) | 0.55 (0.38–0.75) |

Correlations across states, with 90% intervals; corrected for sampling error they are higher by at most 0.03.

**Mobility.** Mobility into formal and better-paid work is a stable feature of each state across two decades, including the pandemic and the change in survey design in 2020. P39 is supported. Exits from employment vary more from period to period.

### 4.3 Mobility and growth

| Test | States | Spearman ρ | 90% interval |
|---|---|---|---|
| M1 2005–2011 vs growth 2012–2019 (P40) | 30 | 0.32 | 0.01 to 0.55 |
| conditional on initial GDP per person and formal share | 30 | 0.33 | 0.00 to 0.60 |
| M2 instead of M1 | 30 | 0.31 | 0.01 to 0.58 |
| M3 (exits) instead of M1 | 30 | −0.36 | −0.62 to −0.04 |
| all 32 states | 32 | 0.39 | 0.10 to 0.59 |
| all 32 states, non-oil GDP | 32 | 0.40 | 0.10 to 0.61 |
| M1 2005–2011 vs growth 2005–2019 | 30 | −0.02 | −0.31 to 0.27 |

**The main test.** States with more informal-to-formal mobility in 2005–2011 grew faster over 2012–2019. P40 is supported, narrowly: the lower end of the interval is 0.01.
- **Consistency:** the direction is consistent across measures. States with more upward moves grew faster; states with more exits grew more slowly.
- **Influence:** no single state drives the result. Leaving out one state at a time gives correlations from 0.26 to 0.37.
- **Controls:** conditioning on initial GDP per person and the formal share does not change it.

**The full period.** Over 2005–2019 as a whole there is no relation. Mobility measured in 2005–2011 is unrelated to growth over the same years and the following ones combined. This suggests that what tracks later growth is not past growth that mobility merely reflects. It also shows how sensitive a correlation over 30 states is to the window chosen.

## 5. Robustness and limits

- **Composition.** The adjustment covers age, sex, schooling, sector, formality and urban residence. Unobserved differences between states' workers, or in what "formal" means locally, are not covered: the share of formal jobs in public employment differs, for example. This is one possible reason for Guerrero's high rate.
- **Residence and migration.** People are assigned to their state of residence. Workers who move between states leave the panel and are not counted.
- **GDP per person.** Population comes from ENOE's weights. These follow official projections calibrated to the 2010 census, and growth in GDP per person depends on them. In Querétaro, for example, population grew faster (2.8% a year) than GDP (2.1%) over 2012–2019.
- **Inference with 30 states.** A rank correlation of 0.32 among 30 states is weak evidence. The interval barely excludes zero, and other windows give different answers (§4.3). It describes co-movement. Many state characteristics could drive both mobility and growth, such as industrial structure, links to US markets or the quality of local institutions.

## 6. Conclusions

**Mobility differs by state.** Mexican states differ substantially in how often workers move from informal to formal work, or into better-paid types of job, for the same workforce composition. The differences are almost entirely real and very stable: the state ranking in 2022–2025 is nearly the same as in 2005–2011.

**Mobility and the formal sector.** Mobility is unrelated to the size of the formal sector. States with large formal sectors are not necessarily places where informal workers move into them.

**Mobility and growth.** States with more upward mobility in 2005–2011 grew somewhat faster afterwards, but the relation is weak, depends on the period and cannot be read causally.

**For this programme.** Upward mobility appears to be a stable property of places as well as of jobs (9.1, 9.5). It is related to growth more weakly than it is to itself over time. Identifying what makes some states durable "ladders" would need a different design: variation in state policies, or industries whose location is set by factors unrelated to local mobility.

**What would change these conclusions:**
- state rankings that change once the formality of public employment is accounted for;
- a design that separates the effect of mobility on growth from common causes, for example the location of export manufacturing.

## Annex A. Notes on implementation and further work

**A.1 Choices.**
- **Growth tests.** Non-oil GDP for all 32 states was added after the plan, once the activity detail of PIBE showed it could replace excluding Campeche and Tabasco (decision D-061). So was the leave-one-state-out check.
- **Geography.** State boundaries are dissolved from CONABIO's 2020 municipal boundaries (as in study 9.4).

**A.2 Further work.**
- **Public employment.** Decompose states' informal-to-formal moves by destination (public sector, large private establishments, IMSS registration).
- **Below the state.** Repeat at the level of metropolitan areas (ENOE's self-represented cities), which are closer to local labour markets.
- **External shocks.** Relate mobility to state exposure to US demand (export manufacturing), a source of variation in growth that is not caused by local mobility.

## References

- Donovan, K., Lu, W.J. and Schoellman, T. (2023). Labor market dynamics and development. *Quarterly Journal of Economics* 138(4): 2287–2325. [L160]
- INEGI (2023). *Sistema de Cuentas Nacionales de México: fuentes y metodologías, año base 2018*, §4.3 "Producto Interno Bruto por Entidad Federativa, anual". [L162]
- INEGI (2026). Producto Interno Bruto por Entidad Federativa, base 2018, revised 2024 release, open-data CSV sets. [L163]
