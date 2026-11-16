# Study 9.6 — States: where do workers move up, and does it track growth?

*Paul Wander. Pre-analysis plan v0.1, 2026-11-13. Written before any state-level estimate was computed. State GDP (INEGI, PIBE) has been requested and was not in hand when this plan was written (D-059).*

## 1. Question and propositions

Studies 9.1–9.5 describe how Mexican workers move between jobs. Those moves happen in local labour markets that differ in industry, firm size, formality and growth. If the "rungs" of the job ladder are a property of places as well as of jobs, some states should offer more upward moves than others with the same workforce. Those states might also grow faster.

The study measures, for each of the 32 states, how often workers move up within a year, adjusted for who lives there. It then asks three questions:
- whether the differences between states are larger than sampling error;
- whether they persist over time;
- whether states with more upward moves grew faster.

**P38. States differ in upward mobility beyond composition and sampling error.**
- **Supported if,** for the adjusted one-year informal-to-formal rate in 2005–2011, the estimated variance of true state effects (τ², method of moments) is at least half of the variance of the estimated state effects.
- **Rejected if** it is below a fifth.
- **Inconclusive** otherwise.

**P39. State differences persist.**
- **Supported if** the correlation between states' adjusted informal-to-formal rates in 2005–2011 and in 2012–2018 (start years of the panels), corrected for sampling error (disattenuated), is at least 0.5.
- **Rejected if** it is below 0.2.
- **Inconclusive** otherwise.

**P40. States with more upward moves grew faster afterwards.**
- **Supported if** the rank correlation between the adjusted informal-to-formal rate in 2005–2011 and growth of GDP per person from 2012 to 2019 is positive with a 90% interval above zero. The interval is a bootstrap over states, and the sample is 30 states, excluding Campeche and Tabasco, whose GDP is dominated by oil.
- **Rejected if** the 90% interval is entirely below zero.
- **Inconclusive** otherwise.

With 30 states the test has low power. A correlation of about 0.3 would be needed for the interval to exclude zero.

## 2. Data

- **Survey.** ENOE, every quarter of 2005–2019 (and 2022 onward, for description only).
  - **Panels.** For each starting quarter, persons at their first interview are linked to the fifth, one year later, with the linkage of study 9.1.
  - **Periods.** Panels starting in 2005–2011 (first period) and 2012–2018 (second). Each person is assigned to the state of residence at the first interview.
- **Sample.** Persons aged 16–65 at the first interview, linked to the fifth.
- **Measures**, one year after the first interview:
  - **M1, informal to formal** (primary): among those informally employed at the first interview, the share formally employed at the fifth.
  - **M2, upward move:** among the employed, the share employed one year later in a sector × formality cell with higher national median hourly earnings in the same year. Establishment size is left out because it is misreported (study 9.1).
  - **M3, exit:** among the employed, the share not employed one year later.
- **State GDP.** INEGI's PIBE, base 2018, at constant prices.
- **State population.** All ages, from ENOE survey weights (annual average).

## 3. Estimation

**Adjusted state effects.** For each measure and period, a weighted linear probability model at person level is estimated, with:
- state fixed effects;
- fixed effects for the starting quarter, single years of age, sex, years of schooling (single years), the sector at the first interview (and, for M2 and M3, formality), and urban residence.

The state effects are the adjusted measures. Standard errors are clustered by primary sampling unit.

**Signal and noise.** Over the 32 state effects, τ² is the variance of the estimates minus the mean of their squared standard errors (P38).
- **Persistence (P39):** the correlation between periods, divided by the square root of the product of each period's reliability, where reliability = τ² / variance of the estimates.
- **Empirical Bayes:** state effects are also shrunk by empirical Bayes for the maps and tables.

**Growth (P40).**
- **Main test:** Spearman's rank correlation between the 2005–2011 adjusted M1 and the annual log growth of GDP per person over 2012–2019, with a 90% interval from 1,999 bootstrap resamples of states.
- **Secondary (no proposition):**
  - partial correlations conditional on initial log GDP per person and the initial formal share of employment;
  - the same with M2;
  - the contemporaneous relation over 2005–2019.

## 4. Robustness and description

- **Unadjusted rates.**
- **Urban areas only** (self-represented cities).
- **2022 onward**, compared with 2012–2018 for persistence.
- **Including Campeche and Tabasco.**
- **Description:**
  - maps of adjusted measures by state;
  - the formal share and mean log hourly earnings by state and year;
  - the correlation of M1 with the state's formal share. A high formal share mechanically limits how many workers can move from informal to formal work, so this is reported, not tested.

## 5. What would change the conclusions

- **Commuting and migration.** Assigning people to their state of residence misattributes moves by workers who commute or migrate between states. Movers who change dwelling are lost to the panel, which loses them in any case.
- **Reverse causation (P40).** A positive correlation between mobility and growth could reflect growth that had already started. Using mobility in the earlier period and growth in the later one reduces, but does not remove, this concern.
- **Small numbers.** Thirty states cannot separate mobility from other state characteristics. P40 is a description of co-movement, not an estimate of a causal effect.
