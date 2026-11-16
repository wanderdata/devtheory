# Study 9.7 — Labour productivity growth by state and activity in Mexico, 2005–2024

*Paul Wander. Pre-analysis plan v0.1, 2026-11-16. Written before any productivity estimate by state or activity was computed. Before writing, two feasibility checks were run on ENOE alone: the stability of the industry code over time and the sample size of state × activity cells (Section 2). INEGI's quarterly informal-economy accounts by state (MEITEF) have been requested and were not in hand when this plan was written (D-065).*

## 1. Question and propositions

Mexico's labour productivity grew little over 2005–2024 on average, so national data offer little variation with which to study how productive development happens (research log, session 26). States and activities differ much more. The automotive and aerospace clusters of the Bajío expanded, oil output in Campeche and Tabasco collapsed, and tourism grew in Quintana Roo. This study builds a panel of value added (INEGI's state accounts, PIBE) and employment, hours, earnings and formality (ENOE) by state, activity and year, and uses it to describe where non-oil labour productivity grew, through which channels, and whether workers' earnings and formality moved with it. It is descriptive throughout. Its purpose is to locate the episodes in which productivity did grow, as candidates for designs with stronger identification (OQ-80).

Three propositions are tested. Each could fail given what is known before estimation: the relative size of within-activity growth and reallocation differs across countries and periods in the structural-change literature (McMillan and Rodrik 2011; de Vries, Timmer and de Vries 2015), formalisation in Mexico has been slow and uneven, and pass-through of productivity to pay is contested (Stansbury and Summers 2017).

P41. In states where non-oil labour productivity grew, growth within activities contributed more than reallocation of employment between activities. The test uses the decomposition of Section 3.2 between 2005–2007 and 2017–2019. Among the states with positive growth, P41 is supported if the within term exceeds the reallocation term (static plus dynamic) in at least two thirds of them, rejected if it does so in fewer than one third, and inconclusive otherwise. States whose growth is not distinguishable from zero (90% interval including zero) are reported but not counted.

P42. States with faster growth of non-oil labour productivity had larger increases in the formal share of employment. The test is Spearman's rank correlation across the 31 geographic units (Section 2) between the two changes, from 2005–2007 to 2017–2019, with a 90% interval from 1,999 bootstrap resamples of units. P42 is supported if the interval lies above zero, rejected if the point estimate is below 0.1, and inconclusive otherwise. With 31 units a correlation of about 0.3 is needed for the interval to exclude zero.

P43. Growth of value added per hour in a state and activity is passed through to the hourly product wage of the workers employed there. The test is the slope of the change in the log product wage on the change in log value added per hour, across state × activity cells between 2005–2007 and 2017–2019, with state and activity fixed effects, weighted by initial employment, and corrected for the sampling error of ENOE in the regressor (Section 3.4). P43 is supported if the slope is at least 0.5 and its 90% interval excludes zero, rejected if the upper end of the interval is below 0.5, and inconclusive otherwise.

## 2. Data

Value added comes from PIBE, base 2018, as committed in `empirics/data/source/inegi/` (D-060). It gives gross value added at basic prices for each state, 2003–2024, at constant 2018 prices and at current prices, with implicit price indices, for the total and for INEGI's 41 activities: every two-digit SCIAN sector, primary activities split into crops, livestock, fishing and other, mining split into oil and non-oil, and manufacturing in twelve subsector groups. Oil-mining value added (INEGI's "minería petrolera") is excluded throughout, as are workers coded to oil and gas extraction (ENOE code 2111), so that all measures refer to the non-oil economy. Workers in mining support services (2131), which include oil-well drilling, stay in non-oil mining; excluding them is a robustness check.

Employment, hours, earnings and formality come from ENOE, every quarter of 2005–2019 and 2022–2024, persons aged 15 and over employed in the reference week, assigned to an activity by the industry code of their main job (`p4a`, four-digit SCIAN as coded by INEGI). In the feasibility check on the second quarter of eleven years from 2005 to 2025, the code is present for all employed persons (0.6% missing in 2021), and the shares of the three-digit groups change smoothly, except within construction (SCIAN 236 and 238, 2005–2011) and within retail (SCIAN 469, 2005–2008), shifts that disappear at the level of aggregation used here. Codes 9700, 9800 and 9999 (unspecified, 0.6% of the employed) are distributed across activities within state in proportion to specified employment. Annual values are averages of the four quarters, with the quarterly weights (`fac_tri` where the file has it, otherwise `fac`).

The main activity classification has 20 groups, chosen so that every state × activity cell has a usable sample: agriculture, forestry and fishing (11); non-oil mining (21); utilities (22); construction (23); four manufacturing groups, namely food, beverages and tobacco (311–312), textiles, clothing, leather, wood, paper, printing and furniture (313–316, 321–323, 337), petroleum products, chemicals, plastics, non-metallic minerals and metals (324–327, 331–332), and machinery, electrical and transport equipment and other manufacturing (333–336, 339); wholesale trade (43); retail trade (46); transport and storage (48–49); information (51); finance and insurance (52); real estate (53); professional, corporate and support services (54–56); education (61); health and social assistance (62); accommodation and food (72); arts, recreation and other services (71, 81); and government (93). A fine classification with the 33 PIBE series that ENOE can match is used as a robustness check. In the feasibility check for 2019Q2, the median state × fine-activity cell had about 300 person-quarter observations in a year and a fifth of cells fewer than 100, mostly in wood products, utilities, corporate offices and small manufacturing groups; these are the cells merged in the main classification.

The geographic unit is the state, with Mexico City and the State of Mexico combined into one unit (31 units). PIBE assigns value added to the state where establishments are located, and ENOE assigns workers to the state where they live; the daily commute from the State of Mexico into Mexico City is the largest such mismatch. Results with the two states separate are reported. Smaller cross-state commuting zones (La Laguna across Coahuila and Durango; Puebla and Tlaxcala) are left as they are.

The period comparison uses averages of 2005–2007 and 2017–2019, so that neither endpoint contains the 2008–09 recession or the pandemic. The change from 2017–2019 to 2022–2024 is described but not tested.

## 3. Measures and estimation

### 3.1 Productivity

Labour productivity in a state and activity is real value added (constant 2018 prices) per employed person, and per hour worked in the main job as a robustness check. Aggregate non-oil productivity of a state is total non-oil value added per employed person. Growth is in log points a year.

### 3.2 Decomposition

For each state, the change in aggregate productivity $P = \sum_i s_i p_i$, with $s_i$ the employment share and $p_i$ the productivity of activity $i$, is decomposed as

$$\Delta P = \sum_i s_{i0}\,\Delta p_i + \sum_i p_{i0}\,\Delta s_i + \sum_i \Delta p_i\,\Delta s_i ,$$

the within, static reallocation and dynamic reallocation terms, as in WP05, WP06 and WP08, and the log growth of $P$ is divided between them in proportion to their linear values. The decomposition uses constant 2018 prices; as a check, it is repeated at 2005–2007 prices, obtained from the current-price and volume series of PIBE.

A third term, formalisation, is added by splitting each activity into formal and informal segments (INEGI's labour-informality definition, as in studies 9.1–9.6). The value added of each state is divided between the two segments using MEITEF's informal value added for that state and period, and within the state between activities in proportion to ENOE labour income by activity and segment. The formalisation term is the segment-level reallocation term minus the activity-level reallocation term, as in study 9.3. If MEITEF does not arrive, the split uses labour income alone with θ = 1, as in study 9.3, and the formalisation term is reported as conditional on that assumption. P41 does not depend on this term.

### 3.3 Formality (P42)

The formal share is the share of employed persons aged 15 and over in formal employment, from ENOE, annual average. Its change and the growth of aggregate non-oil productivity are compared across the 31 units with Spearman's correlation, with 1,999 bootstrap resamples of units. The partial correlation given the initial productivity level is reported beside it, without a decision rule.

### 3.4 Pass-through (P43)

The product wage of a cell is mean hourly labour income in the main job of employees and own-account workers with positive reported income, deflated by the PIBE implicit price index of the state and activity. Because earnings reporting fell sharply over the period (study 9.2), the mean is computed with the non-response reweighting of study 9.2 (`profiles/06_reweight.py`), within state, by formality, five-year age group and schooling. The slope is estimated by weighted least squares on cells with at least 100 observations with income in each period. Sampling error in ENOE hours enters value added per hour and attenuates the slope; the slope is corrected by dividing it by the reliability of the regressor (the share of its variance across cells, net of fixed effects, not due to sampling error, estimated from the bootstrap of Section 3.5). Both the corrected and the uncorrected slopes are reported, and the corrected one is used for the test.

### 3.5 Sampling error

PIBE is treated as fixed; INEGI publishes no measure of its error. ENOE quantities carry sampling error. Intervals come from 199 bootstrap replications that resample primary sampling units within states in each quarter, applied to aggregates by PSU, state, activity and segment computed once from the microdata. Intervals for P42 resample the 31 units, as in study 9.6.

## 4. Description

The study reports, without propositions:

1. maps and tables of non-oil productivity growth by state, 2005–2007 to 2017–2019 and 2017–2019 to 2022–2024, per person and per hour;
2. the contribution of each state × activity cell to the growth of national non-oil productivity, and the 15 largest positive and negative contributions;
3. the decomposition for the six states with the fastest and the six with the slowest growth, with the activities behind each term;
4. the cases named in Section 1 (the Bajío states, Campeche and Tabasco with and without oil, and Quintana Roo), with value added, employment, formality and product wages by activity, year by year;
5. a comparison of ENOE employment by activity with the jobs (puestos de trabajo) of MEITEF, when available.

## 5. Robustness

Hours instead of persons; the fine activity classification; mining support services excluded with oil; Mexico City and the State of Mexico separate; the market economy, excluding real estate (whose value added includes imputed rent on owner-occupied dwellings, with almost no employment) and government (whose value added is measured by costs); 2005–2007 prices; the change to 2022–2024; for P43, the uncorrected slope, unweighted cells and the product wage without reweighting.

## 6. What would change the conclusions

The employment denominators come from a household survey and the numerators from establishment-based accounts. Commuting, secondary jobs (whose output is in PIBE but whose workers are counted only in their main activity) and differences between ENOE's industry coding and INEGI's establishment classification all move value added and workers into different cells. They matter most for small cells, which is why the main classification is coarse.

PIBE at state level is partly estimated by distributing national totals with indicators, so some state-level productivity differences may reflect the indicators INEGI uses rather than measured output. Section 4.3 of INEGI's methodology (L162) lists the indicators by activity; the results for activities where the distribution relies on employment indicators are flagged.

Population weights before 2020 follow projections based on the 2010 census (OQ-79). Levels of employment by state are affected; shares within states, which drive the decomposition, much less.

None of the comparisons identifies causes. The decomposition is an accounting identity, and the correlations in P42 and P43 can arise from common shocks, from changes in the composition of workers within cells, or from causation in either direction.

## Addendum A1 (2026-11-16): use of MEITEF

Written after MEITEF arrived and before any productivity estimate was computed; the only figures examined were MEITEF's own consistency checks (states sum to the national total; activities sum to the state total).

MEITEF gives informal-economy value added, at constant 2018 and current prices, for each state and 19 activities (two-digit SCIAN sectors, with manufacturing as one sector, wholesale and retail trade combined, and corporate and support services combined), annually 2005–2025, together with paid informal jobs and pay. Its informal economy is the informal sector plus other informal employment, which corresponds to INEGI's labour-informality definition used for formality in ENOE. The split of Section 3.2 is therefore made as follows: the informal value added of a state and activity is MEITEF's, and formal value added is PIBE's non-oil value added minus MEITEF's; where the plan's activity groups are finer than MEITEF's (the four manufacturing groups, wholesale and retail, and professional, corporate and support services), MEITEF's informal value added is divided among them in proportion to the informal labour income of each group in ENOE. Where MEITEF's informal value added exceeds PIBE's for a group, which can happen through rounding in small cells, the group is treated as wholly informal and the case is reported.

MEITEF is compiled partly from ENOE, so formal and informal productivity are not independent of the survey used for employment. The formalisation term measured this way rests on INEGI's allocation of value added between the segments, which uses the economic censuses and the national accounts, rather than on an assumed gap. The θ = 1 split of study 9.3 is reported as a comparison.
