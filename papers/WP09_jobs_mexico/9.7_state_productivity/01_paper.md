# Labour Productivity Growth by State and Activity in Mexico, 2005–2019

*Paul Wander. Working draft v0.1, 2026-11-16. Pre-analysis plan: [`00_pre_analysis_plan.md`](00_pre_analysis_plan.md) (with addendum A1). Generated tables: [`empirics/output/enoe/state_productivity/results.md`](../../../empirics/output/enoe/state_productivity/results.md). App: Jobs in Mexico, page 9.7.*

## Abstract

Mexico's non-oil labour productivity grew by 0.08 log points a year between 2005–2007 and 2017–2019, so national data say little about how productivity grows. This paper uses the variation across states and activities instead. It combines value added from INEGI's state accounts (PIBE, base 2018, 31 geographic units, 20 activity groups) with employment, hours, earnings and formality from the labour-force survey (ENOE), and informal value added from INEGI's informal-economy accounts by state (MEITEF). Growth of non-oil value added per employed person ranged from 1.45 log points a year in Zacatecas (90% interval 1.28 to 1.65) to −2.34 in Campeche (−2.49 to −2.20); it was positive in 13 units. In 12 units growth was distinguishable from zero, and in 9 of these the reallocation of employment between activity groups contributed more than growth within groups, so the proposition that within-group growth dominated is rejected under the plan's rule; at 2005–2007 prices the result is inconclusive. Across units, productivity growth has a rank correlation of 0.71 (0.52 to 0.83) with the increase in the formal share of employment, and of 0.53 and 0.58 when the two variables are estimated from independent halves of the survey sample. Across state × activity cells, the hourly product wage grew by 0.16% (0.06 to 0.24) for each 1% of growth in value added per hour, after correction for sampling error. All results are descriptive, and the comparison of value added from establishment-based accounts with employment from a household survey is the main source of measurement error.

## 1. Introduction

Earlier work in this programme found that the characteristics of jobs recorded in ENOE predict workers' trajectories poorly (studies 9.1–9.6). A plausible reason is that Mexico's productivity hardly grew in the period studied, so there was little growth for job characteristics to be associated with (open question OQ-80). National averages, however, conceal large differences. In the states of the Bajío, automotive and aerospace manufacturing expanded; in Campeche and Tabasco, oil output fell sharply; in Quintana Roo, employment in tourism grew quickly. These are the episodes in which productive development might be observed.

The paper describes where non-oil labour productivity grew across Mexican states between 2005–2007 and 2017–2019, through which channels, and whether workers' formality and pay moved with it. It applies the shift-share decomposition used in WP05, WP06 and WP08 (McMillan and Rodrik 2011; de Vries, Timmer and de Vries 2015), adds a term for the movement of workers from informal to formal segments within activities, measured with INEGI's informal-economy accounts by state, and tests three propositions set out in a pre-analysis plan before any estimate was computed. Section 2 describes the data, Section 3 the method, Section 4 the results and Section 5 the limitations.

## 2. Data

Value added comes from INEGI's state accounts (Producto Interno Bruto por Entidad Federativa, base 2018), which give gross value added at basic prices by state and 41 activities, 2003–2024, at constant 2018 prices and at current prices. Oil-mining value added (INEGI's "minería petrolera") is excluded, together with ENOE workers in oil and gas extraction (0.1% of employment), so all measures refer to the non-oil economy. The 34 activity series that ENOE's industry code can be matched to add up exactly to non-oil gross value added in every state and year.

Employment, hours, labour income and formality come from ENOE, every quarter of 2005–2019 and 2022–2024, for persons aged 15 and over. Each employed person is assigned to an activity by the four-digit industry code of the main job. Codes that do not identify an activity (2.3% of employment, including code 3380, which ENOE uses mostly in the northern border states) are distributed within state, period and formality segment in proportion to specified employment. Formality follows INEGI's labour-informality definition. Period values are averages over 2005–2007 (P0), 2017–2019 (P1) and 2022–2024 (P2); neither of the first two contains the 2008–09 recession or the pandemic.

Informal value added comes from INEGI's quarterly measurement of the informal economy by state (MEITEF, base 2018), which gives the value added of the informal sector and of other informal employment for each state and 19 activities. The informal economy in MEITEF corresponds to the labour-informality definition used for ENOE. Where an activity group of this paper is finer than MEITEF's (four manufacturing groups; wholesale and retail trade), MEITEF's informal value added is divided among the groups in proportion to ENOE informal labour income. MEITEF is compiled partly from ENOE.

The 20 activity groups were chosen so that every state × group cell has a usable sample; a classification with the 34 series is used as a robustness check. The geographic unit is the state, with Mexico City and the State of Mexico combined (31 units), because PIBE assigns value added to the place of production and ENOE assigns workers to their place of residence, and the commute between these two states is the largest such mismatch.

## 3. Method

Aggregate labour productivity of a unit, $P=\sum_i s_i p_i$, is non-oil value added per employed person, with $s_i$ the employment share and $p_i$ the productivity of group $i$. Its change is decomposed into a within term $\sum_i s_{i0}\Delta p_i$, a static reallocation term $\sum_i p_{i0}\Delta s_i$ and a dynamic reallocation term $\sum_i \Delta p_i \Delta s_i$, and the log growth of $P$ is divided among them in proportion to their linear values. Splitting each group into formal and informal segments gives a segment-level decomposition; the formalisation term is the reallocation term of the segment-level decomposition minus that of the group-level one. Growth and its components are in log points a year over the twelve years between the midpoints of P0 and P1.

PIBE and MEITEF are treated as fixed. ENOE quantities carry sampling error, which is estimated with 199 bootstrap replications that draw primary sampling units with replacement within state and period, the same draw applying to every quarter of a period because ENOE revisits dwellings, and that are calibrated to the state's weighted population aged 15 and over, as ENOE's weights are.

Three propositions were tested. P41: in units whose productivity grew, the within term exceeded reallocation (static plus dynamic); supported if this holds in at least two thirds of the units whose growth is positive with a 90% interval above zero, rejected if in fewer than one third. P42: units with faster productivity growth had larger increases in the formal share of employment; Spearman's correlation across the 31 units, supported if its 90% interval (1,999 resamples of units) lies above zero, rejected if the estimate is below 0.1. P43: growth of value added per hour in a unit × group cell is passed through to the hourly product wage; supported if the slope, with unit and group fixed effects, weighted by initial employment and corrected for sampling error in the regressor, is at least 0.5 with an interval excluding zero, rejected if the upper end of the interval is below 0.5. The product wage is mean hourly labour income in the main job of employees and own-account workers, deflated by the PIBE price index of the state and group and adjusted for earnings non-response by weighting classes of year, state, formality, age and schooling.

## 4. Results

### 4.1 Growth by state

Non-oil labour productivity in Mexico grew by 0.08 log points a year between P0 and P1. The national series is flat apart from the fall of 2009, a recovery in 2010–2011 and a decline in 2019, when ENOE employment grew by 2.7% and value added barely changed. Across the 31 units, growth ranged from 1.45 log points a year in Zacatecas to −2.34 in Campeche (Table 1). It was positive in 13 units and, with sampling error taken into account, distinguishably positive in 12. The fastest growth was in a band of central and northern states: Zacatecas, San Luis Potosí, Aguascalientes, Chihuahua, Guanajuato and Sinaloa, all between 0.70 and 1.45. The largest declines were in Campeche, Baja California, Oaxaca, Nayarit and Hidalgo. The sampling error of a unit's growth rate is small, with a standard deviation of about 0.09 log points a year, so the differences between units are not a product of the survey sample.

*Table 1. Growth of non-oil labour productivity and its components, selected units, 2005–2007 to 2017–2019 (log points a year)*

| Unit | Growth (90% interval) | Within | Static | Dynamic | Formalisation | Change in formal share (pp) |
|---|---|---|---|---|---|---|
| Zacatecas | 1.45 (1.28 to 1.65) | 0.38 | 1.40 | −0.33 | −0.10 | 5.2 |
| San Luis Potosí | 1.24 (1.11 to 1.39) | 0.56 | 0.93 | −0.24 | 0.11 | 6.7 |
| Aguascalientes | 1.22 (1.11 to 1.32) | 0.39 | 1.14 | −0.31 | 0.19 | 3.7 |
| Chihuahua | 0.99 (0.82 to 1.15) | 0.21 | 1.32 | −0.55 | 0.01 | 5.0 |
| Guanajuato | 0.73 (0.57 to 0.89) | −0.07 | 1.57 | −0.77 | 0.11 | 5.8 |
| Michoacán | 0.67 (0.46 to 0.87) | 1.24 | −0.28 | −0.29 | −0.04 | 2.3 |
| Querétaro | 0.26 (0.10 to 0.41) | −0.33 | 1.39 | −0.80 | 0.18 | 5.8 |
| Mexico City and State of Mexico | 0.23 (0.15 to 0.31) | 0.13 | 0.17 | −0.07 | 0.11 | 0.4 |
| Nuevo León | −0.12 (−0.21 to −0.01) | −0.24 | 0.28 | −0.16 | 0.14 | 2.8 |
| Quintana Roo | −0.34 (−0.43 to −0.25) | −0.46 | 0.43 | −0.31 | 0.09 | 3.5 |
| Tabasco | −0.84 (−1.03 to −0.66) | 0.27 | −0.13 | −0.99 | −2.07 | −2.6 |
| Oaxaca | −1.55 (−1.73 to −1.35) | −1.61 | 0.23 | −0.17 | −0.16 | −1.0 |
| Baja California | −1.65 (−1.75 to −1.54) | −1.80 | 0.58 | −0.43 | −0.04 | 1.1 |
| Campeche | −2.34 (−2.49 to −2.20) | −2.46 | 0.23 | −0.12 | −0.22 | −2.4 |
| Mexico | 0.08 | −0.26 | 0.50 | −0.16 | 0.12 | 2.1 |

*Within, static and dynamic add up to growth. The formalisation term belongs to the segment-level decomposition, in which within-segment growth replaces the within term. All 31 units are in the generated tables.*

### 4.2 Within-activity growth and reallocation

In Mexico as a whole, productivity within activity groups fell by 0.26 log points a year and the movement of workers towards groups with higher productivity levels added 0.50, partly offset by a dynamic term of −0.16: the groups whose employment share rose tended to be those whose productivity fell. The same pattern appears in most states, and it is the pattern that de Vries, Timmer and de Vries (2015) describe for Africa as static gains and dynamic losses.

Part of the dynamic term is an artefact of measurement. Sampling error in a group's employment moves its employment share and its measured productivity in opposite directions, which biases the dynamic term downwards and the static term upwards. The bootstrap gives an estimate of this bias: on average across units, −0.16 log points a year for the dynamic term, +0.10 for the static term and +0.06 for the within term. The national dynamic term is therefore of the same size as its bias, while the static term remains positive after correction.

Among the 12 units with growth distinguishably above zero, the within term was larger than reallocation in three (Michoacán, Colima, and Mexico City with the State of Mexico); in the other nine, including the four Bajío states, Zacatecas and Chihuahua, reallocation contributed more. With each term corrected for bias, the count falls to two. The split between within and reallocation depends on relative prices: at 2005–2007 prices, which give more weight to activities whose prices have since fallen relative to others, the within term exceeds reallocation in six of the 12 units and the median within term across all units is positive (0.07) rather than negative (−0.24). With the fine classification the count is four of 12, and with hours instead of persons four of the 10 eligible units.

### 4.3 Productivity growth and formalisation

The formal share of non-oil employment rose from 41.3% to 43.4% nationally, and by more in units whose productivity grew faster. The Spearman correlation across the 31 units is 0.71 (90% interval 0.52 to 0.83), and 0.77 (0.59 to 0.86) holding initial productivity constant. Both variables use ENOE employment, so common sampling error could generate a correlation. Estimated with productivity growth from one half of the primary sampling units and the change in the formal share from the other half, the correlation is 0.58 and 0.53 in the two combinations, and 0.49 and 0.54 within each half, so it is not produced by sampling error shared between the two variables.

The formalisation term, which measures how much aggregate productivity rose because workers moved from informal to formal segments within activity groups, was 0.12 log points a year nationally, and its median across units was 0.02. It is negative and large in Tabasco (−2.07), where the formal share of employment fell by 2.6 points, and in Tlaxcala (−1.14). Its value rests on INEGI's allocation of value added between the formal and informal segments in MEITEF.

### 4.4 Productivity and pay

Across 582 unit × group cells, a change of 1% in value added per hour is associated with a change of 0.09% in the hourly product wage (90% interval 0.03 to 0.14), with unit and group fixed effects and employment weights. Sampling error in ENOE hours accounts for 43% of the variance of the regressor after the fixed effects are removed; correcting for it raises the slope to 0.16 (0.06 to 0.24). Without employment weights the uncorrected slope is 0.12, and without the adjustment for earnings non-response, 0.09. Productivity growth within a state and activity was therefore associated with some growth in pay relative to the activity's own output prices, but with less than a fifth of it.

### 4.5 Named cases

In the four Bajío states, productivity grew by 0.26 (Querétaro) to 1.24 (San Luis Potosí) log points a year, and employment by 1.9% to 2.8% a year. In each of them the group of machinery, electrical and transport equipment at least doubled its share of state employment (in Guanajuato from 1.5% to 4.8%, in Aguascalientes from 5.0% to 10.2%), and this movement into a group with above-average productivity is the largest reallocation term in each state (from 0.51 log points a year in Querétaro to 1.08 in Aguascalientes). The measured productivity of the group itself fell in three of the four states, by 1.3 to 5.3 log points a year, because ENOE employment in it grew faster than PIBE value added at constant prices. In Querétaro, for example, ENOE employment in the group rose from about 40,000 in 2005–2007 to 85,000 in 2017–2019 while its value added at constant prices rose by 11%. Whether this reflects the entry of plants with lower value added per worker, a change in the relative price of transport equipment, or a difference in coverage between the household survey and the economic censuses on which PIBE rests cannot be settled with these data.

In Campeche, non-oil productivity fell by 2.34 log points a year, mainly within construction (−1.88), which in Campeche depends on oil investment; including oil, it fell by 5.79. In Tabasco the corresponding figures are −0.84 and −1.34. In Quintana Roo employment grew by 4.1% a year and the share of accommodation and food rose from 17.5% to 21.9%; non-oil productivity fell by 0.34 log points a year.

Nationally, the largest positive contributions to growth came from finance and insurance and information in Mexico City and the State of Mexico (0.09 and 0.04 log points a year) and from the expansion of the machinery and transport equipment group in Guanajuato, Chihuahua and San Luis Potosí. Eight of the 15 largest negative contributions came from the group of petroleum products, chemicals, minerals and metals, whose measured productivity fell by 2.4 to 7.7 log points a year in those units.

### 4.6 Propositions

Under the decision rules of the pre-analysis plan, P41 (within-activity growth dominated in the states that grew) is rejected: the within term was larger in 3 of 12 eligible units, against a threshold of one third. The verdict is not robust: it becomes inconclusive at 2005–2007 prices (6 of 12), with the fine classification (4 of 12) and with hours (4 of 10). P42 (faster productivity growth with larger increases in the formal share) is supported, with a lower interval bound of 0.52 against a threshold of zero. P43 (pass-through of at least 0.5) is rejected: the corrected slope is 0.16 and the upper end of its interval 0.24.

## 5. Limitations

Value added comes from establishment-based accounts and employment from a household survey. Commuting, secondary jobs (whose output is in PIBE but whose workers are counted only in their main activity) and differences between ENOE's industry coding and the classification of establishments in the economic censuses all move value added and workers into different cells. They matter most for small cells and for activities, such as manufacturing in the northern states, where ENOE uses a code (3380) that does not identify the subsector. The Bajío results in Section 4.5 could be checked against employment in the economic censuses of 2004 and 2019.

PIBE at state level is partly built by distributing national totals with indicators, and its own error is not published; it is treated here as exact. Productivity growth at constant 2018 prices weights activities by 2018 relative prices, and the division between within growth and reallocation changes when earlier prices are used.

ENOE's population weights before 2020 follow projections based on the 2010 census and those from 2020 on the 2020 census. This affects levels of employment by state between P0 and P1 less than it affects the comparison with 2022–2024, where the change of basis coincides with a fall in measured productivity of 1.29 log points a year in the median unit; that comparison is not interpreted here (open question OQ-79).

None of the results identifies causes. The decomposition is an accounting identity, and the correlations of Sections 4.3 and 4.4 can arise from common shocks, from changes in the composition of workers within cells or from causation in either direction.

## 6. Conclusions

Between 2005–2007 and 2017–2019 non-oil labour productivity grew in about two fifths of Mexico's states and fell in the rest, with a difference of almost four log points a year between the extremes. Where it grew, it grew mainly because employment moved towards activities with higher productivity, in particular to transport-equipment and related manufacturing in the Bajío, while measured productivity within most activities stagnated or fell. States whose productivity grew more also formalised more, and this association does not come from shared sampling error. Workers in the state-activity cells whose productivity grew saw their pay rise relative to the prices of what they produced, but by a small fraction of the productivity gain. The episodes that the national average conceals are therefore episodes of reallocation more than of rising productivity within activities. Examining them further requires data on establishments: the economic censuses to check the employment counts, and the IMSS records of formal employment to follow the workers who moved into the expanding activities.

## Annex A. Implementation notes and departures from the plan

These choices were made after the plan was written and are recorded in decision D-067.

1. The first bootstrap drew primary sampling units without calibrating the replicates to population. Because ENOE's weights are calibrated to population totals, this overstated the sampling error of state employment (a sampling standard deviation of state growth of 0.68 log points a year, against 0.09 with calibration) and left only four units eligible for the test of P41, in none of which the within term dominated. The calibrated bootstrap is used throughout.
2. The split-sample check of P42 was added after the main estimate had been seen, because ENOE employment enters both variables.
3. The bias of the decomposition terms (Section 4.2) was estimated after the results had been seen. The decision rule of P41 is applied to the uncorrected terms, as planned.
4. Informal value added from MEITEF was allocated at the level of the 20 groups, as the plan states. In 41 of the 1,860 unit × group × period cells (33 of them in the group of textiles, clothing, wood, paper and furniture), the allocated informal value added exceeded PIBE value added and was set equal to it. ENOE informal labour income thus assigns more of MEITEF's informal manufacturing value added to this group than PIBE's value added allows.
5. Earnings non-response was adjusted with weighting classes (year, state, formality, five-year age group and schooling level), a saturated version of the covariates used in study 9.2, with classes of fewer than 20 respondents merged into year × state × formality. Reported income of zero was treated as non-response.
6. For the tests, unspecified industry codes were distributed within state, period and segment; for the annual panel, within state, year and segment. The fine classification has 34 series, not the 33 stated in the plan.
7. The descriptive comparison of 2017–2019 with 2022–2024 is affected by the change of ENOE's weighting basis (Section 5).
8. ENOE codes oil and gas extraction as 2110, not 2111 as the plan states. A first run with 2111 left about 35,000 oil workers in non-oil mining; it was replaced before results were reported.

Further work: check the Bajío employment counts against the economic censuses; decompose the reallocation into the machinery and transport equipment group by formality and establishment size; use the comparison of ENOE informal employment with MEITEF's informal jobs by state and activity to assess coverage; and, as a design with stronger identification, relate the expansion of transport-equipment manufacturing to the location of plant openings that were decided outside local labour markets.

## References

de Vries, G., Timmer, M. and de Vries, K. (2015). Structural transformation in Africa: static gains, dynamic losses. *Journal of Development Studies* 51(6): 674–688. [L118]

INEGI (2026a). Producto Interno Bruto por Entidad Federativa, base 2018, revised 2024 release, open-data files. [L163]

INEGI (2026b). Mediciones de la Economía Informal Trimestral por Entidad Federativa, base 2018, tabulados 2005Q1–2026Q1. [L168]

McMillan, M. and Rodrik, D. (2011). Globalization, structural change and productivity growth. NBER Working Paper 17143. [L018]

Stansbury, A. and Summers, L.H. (2017). Productivity and pay: is the link broken? NBER Working Paper 24165. [L167]
