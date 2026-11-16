# Job Mobility and Growth across Mexican States, 2005–2025

*Paul Wander. Working draft v0.2, 2026-11-16. Pre-analysis plan: [`00_pre_analysis_plan.md`](00_pre_analysis_plan.md). Generated tables: [`empirics/output/enoe/states/results.md`](../../../empirics/output/enoe/states/results.md). App: Jobs in Mexico, page 9.6.*

## Abstract

This paper measures one-year job mobility in each of Mexico's 32 states with the rotating panel of the national labour-force survey (ENOE), 2005–2025, using 2.8 million persons aged 16–65 observed at their first and fifth interviews. The main measure is the share of informally employed persons who are formally employed one year later, adjusted for age, sex, schooling, sector and urban residence. In panels starting in 2005–2011 the adjusted rate ranges across states from 6.3% (Querétaro) to 19.1% (Guerrero), with a mean of 12.3%; sampling error accounts for about 2% of the variance across states. The state ranking is stable: the correlation between the 2005–2011 and 2012–2018 panels is 0.96 (90% interval 0.93–0.98). Across the 30 states other than Campeche and Tabasco, the 2005–2011 rate has a Spearman correlation of 0.32 (90% interval 0.01–0.55) with growth of GDP per person over 2012–2019, measured with INEGI's state accounts. The relation is not present for growth over 2005–2019 as a whole, and none of the estimates is causal.

## 1. Introduction

Studies 9.1 to 9.5 of this programme describe how Mexican workers move between jobs. These moves take place in local labour markets that differ in industrial structure, establishment size, the extent of informal employment and economic growth. If workers with the same characteristics move into formal or better-paid employment more often in some states than in others, mobility is partly a property of places. A natural question, close to the one that motivated the programme, is whether states in which workers move up more often also grow faster.

Cross-country evidence shows higher rates of job finding and job loss, and less movement into better-paid jobs, in poorer countries (Donovan, Lu and Schoellman 2023). Differences in productivity and growth between Mexican regions are well documented; differences in individual job mobility between states, measured with comparable panel data, have received less attention.

The paper estimates composition-adjusted mobility rates for each state and tests three propositions stated in the pre-analysis plan before any state-level estimate was computed: that state differences exceed what composition and sampling error would produce (P38), that they persist over time (P39), and that states with more mobility in 2005–2011 grew faster in 2012–2019 (P40). Section 2 describes the data, Section 3 the estimation, Section 4 the results and Section 5 the main limitations.

## 2. Data

The mobility measures come from ENOE for every quarter of 2005–2019 and 2022–2026. Each dwelling in ENOE is interviewed in five consecutive quarters. Persons aged 16–65 at their first interview are linked to their fifth interview, one year later, by dwelling, household and person identifiers with checks on sex and age; 76% of persons are linked. Linked persons are grouped by the year of the first interview into panels starting in 2005–2011, 2012–2018 and 2022–2025, and assigned to their state of residence at the first interview.

Three measures are computed, each one year after the first interview:

- M1, the share formally employed among those informally employed at the first interview (INEGI's labour-informality definition);
- M2, the share employed in a cell of sector × formality whose national median hourly earnings in the year of the first interview exceed those of the person's initial cell, among those employed at the first interview. Establishment size is not used to define cells because it is reported with substantial error (study 9.1);
- M3, the share not employed among those employed at the first interview.

M1 is computed on about 374,000 informally employed persons in the 2005–2011 panels and 370,000 in the 2012–2018 panels.

GDP comes from INEGI's state accounts (Producto Interno Bruto por Entidad Federativa, base 2018), at constant 2018 prices. INEGI compiles state GDP from establishment-level data in the economic censuses, surveys and administrative records, assigning the value added of each establishment to the state in which it is located; the 32 states sum to the national total in every year. Oil-mining value added, which in 2019 accounted for 74% of GDP in Campeche and 37% in Tabasco, is available separately and is subtracted to obtain non-oil GDP. Population, all ages, is the annual average of ENOE's weighted totals.

## 3. Estimation

For each measure and period, a weighted linear probability model is estimated on persons, with a full set of 32 state indicators and fixed effects for the quarter of the first interview, single years of age, sex, single years of schooling, the sector of employment at the first interview, formality at the first interview (for M2 and M3) and urban residence (ENOE's self-represented cities). The adjusted rate for a state is its predicted rate at the national average of the other covariates. Standard errors are clustered by primary sampling unit.

The variance of the true state effects, τ², is estimated as the variance of the 32 adjusted rates minus the mean of their squared standard errors; the signal share is τ² divided by the variance of the estimates. Persistence is the correlation of adjusted rates between periods, reported with a 90% interval from 1,999 bootstrap resamples of states, and corrected for sampling error by dividing by the square root of the product of the two signal shares.

Growth of GDP per person is measured in log points a year. The test of P40 is Spearman's rank correlation between the adjusted M1 of the 2005–2011 panels and growth over 2012–2019, across the 30 states other than Campeche and Tabasco, with a 90% interval from 1,999 bootstrap resamples of states. Partial rank correlations condition on log GDP per person in 2012 and the average formal share of employment in 2005–2011.

## 4. Results

### 4.1 Differences between states

Table 1 summarises the adjusted rates for the 2005–2011 panels.

*Table 1. Adjusted one-year mobility rates by state, panels starting in 2005–2011*

| Measure | Mean across states | Standard deviation | Minimum | Maximum |
|---|---|---|---|---|
| M1, informal to formal | 12.3% | 3.2 pp | 6.3% (Querétaro) | 19.1% (Guerrero) |
| M2, move to a higher-paid cell | 13.7% | 2.0 pp | 9.9% | 17.3% |
| M3, exit to non-employment | 14.1% | 1.4 pp | 10.5% | 16.9% |

With samples of this size, sampling error is small relative to the differences between states. For M1 the variance of the estimates is about fifty times the mean sampling variance, so that the estimated signal share is 0.98; it is 0.96 for M2 and 0.94 for M3. Adjustment for composition matters most for M2, whose variance across states is 3.7 times larger after adjustment than before, which indicates that differences in workforce composition partly offset differences in mobility between states.

The informal-to-formal rate is not related to the size of a state's formal sector: its rank correlation with the formal share of employment in 2005–2011 is −0.01 (90% interval −0.30 to 0.28). Querétaro and Coahuila have formal shares of 53% and 60%, and the lowest and fifth-lowest rates; Guerrero, Puebla and Tlaxcala have formal shares between 24% and 29% and rates between 14% and 19%. The adjusted rates estimated only on urban residents have a correlation of 0.92 (2005–2011) and 0.93 (2012–2018) with the main estimates.

### 4.2 Persistence

*Table 2. Correlation of adjusted state rates between periods (90% bootstrap interval)*

| Measure | 2005–2011 and 2012–2018 | 2012–2018 and 2022–2025 |
|---|---|---|
| M1, informal to formal | 0.96 (0.93–0.98) | 0.97 (0.96–0.99) |
| M2, move to a higher-paid cell | 0.93 (0.89–0.96) | 0.93 (0.88–0.97) |
| M3, exit to non-employment | 0.61 (0.26–0.77) | 0.55 (0.38–0.75) |

The rankings of states by M1 and M2 are nearly the same across the three periods, which span the change of survey design in 2020 and the pandemic. Correcting for sampling error raises the correlations by at most 0.03. Exit rates are less stable.

### 4.3 Mobility and subsequent growth

*Table 3. Spearman correlations between mobility and growth of GDP per person (90% bootstrap interval)*

| Specification | States | ρ | 90% interval |
|---|---|---|---|
| M1 2005–2011, growth 2012–2019 (test of P40) | 30 | 0.32 | 0.01 to 0.55 |
| Partial, given log GDP per person 2012 and formal share 2005–2011 | 30 | 0.33 | 0.00 to 0.60 |
| M2 2005–2011, growth 2012–2019 | 30 | 0.31 | 0.01 to 0.58 |
| M3 2005–2011, growth 2012–2019 | 30 | −0.36 | −0.62 to −0.04 |
| M1 2005–2011, growth 2012–2019, all states | 32 | 0.39 | 0.10 to 0.59 |
| M1 2005–2011, growth of non-oil GDP per person 2012–2019, all states | 32 | 0.40 | 0.10 to 0.61 |
| M1 2005–2011, growth 2005–2019 | 30 | −0.02 | −0.31 to 0.27 |

States with higher informal-to-formal and upward mobility in 2005–2011 grew somewhat faster in GDP per person over 2012–2019, and states with higher exit rates grew more slowly. The correlation of 0.32 is not driven by a single state: omitting one state at a time gives values between 0.26 and 0.37. It changes little when initial income and the formal share are held constant, and is slightly higher when Campeche and Tabasco are included, with or without oil.

The relation depends on the period over which growth is measured. Mobility in 2005–2011 is unrelated to growth over 2005–2019 taken as a whole (ρ = −0.02), which implies that states with high mobility grew relatively slowly in 2005–2012. With 30 observations and a correlation of this size, the choice of window can change the conclusion.

### 4.4 Propositions

Under the decision rules of the pre-analysis plan, P38 is supported (signal share 0.98 against a threshold of 0.5), P39 is supported (disattenuated correlation 0.97 against a threshold of 0.5) and P40 is supported, with the lower end of the 90% interval at 0.01. P38 was a weak test: with the sample sizes available, a signal share near one was to be expected whenever states differed at all.

## 5. Limitations

The adjustment holds constant age, sex, schooling, sector, formality and urban residence. Differences between states in unobserved characteristics of workers, or in the composition of formal employment, are not held constant. In particular, the share of public employment in formal jobs differs across states and may account for part of the high rates in Guerrero and other southern states.

Persons are assigned to their state of residence at the first interview. Workers who change dwelling leave the ENOE panel and are not observed one year later, so mobility that involves migration between states is not measured.

GDP per person uses ENOE's population totals, which before 2020 follow official projections based on the 2010 census. Growth of GDP per person is sensitive to them; in Querétaro, for example, population grew by 2.8% a year in 2012–2019 and GDP by 2.1%.

The correlations in Section 4.3 describe co-movement. Industrial structure, exposure to US demand, infrastructure and the quality of state institutions could affect both mobility and growth, and 30 observations cannot separate them.

## 6. Conclusions

Mexican states differ in how often workers of given characteristics move from informal to formal employment or into better-paid types of job, and these differences have been stable for two decades. They are not a reflection of the size of the formal sector. States with more mobility in 2005–2011 grew somewhat faster in GDP per person in 2012–2019, but the correlation is modest, depends on the period and is not evidence of an effect of mobility on growth. Explaining why some states provide more mobility than others would require variation in state policies or in industry location that is unrelated to local labour-market conditions.

## Annex A. Implementation notes and further work

Two analyses were added after the plan (decision D-061): the growth test with non-oil GDP for all 32 states, made possible by the activity detail in INEGI's state accounts, and the leave-one-state-out range for the test of P40. State boundaries for the maps are dissolved from CONABIO's 2020 municipal boundaries, as in study 9.4.

Further work could decompose informal-to-formal moves by destination (public sector, large private establishments, registration with IMSS) and test whether the state ranking survives the exclusion of public employment; repeat the analysis for metropolitan areas (ENOE's self-represented cities), which are closer to local labour markets; and relate mobility to state exposure to US demand for manufactures as a source of variation in growth that does not originate in local labour markets. The effect of using INEGI's reweighted ENOE factors for 2005–2019 on growth of GDP per person should also be assessed (open question OQ-79).

## References

Donovan, K., Lu, W.J. and Schoellman, T. (2023). Labor market dynamics and development. *Quarterly Journal of Economics* 138(4): 2287–2325. [L160]

INEGI (2023). *Sistema de Cuentas Nacionales de México: fuentes y metodologías, año base 2018*, section 4.3, "Producto Interno Bruto por Entidad Federativa, anual". [L162]

INEGI (2026). Producto Interno Bruto por Entidad Federativa, base 2018, revised 2024 release, open-data files. [L163]
