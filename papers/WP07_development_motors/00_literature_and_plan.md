# WP07 — Development motors: literature and pre-analysis plan

*Paul Wander. v0.1, 2026-11-09. Written before any estimation, so that the tests and what would count as support or rejection are fixed in advance (D-037).*

**Questions.**
1. Is manufacturing still a motor of development?
2. Was it ever one in Latin America and the Caribbean?
3. Why does it work only in some contexts?
4. Do other sectors, especially services, act as motors, and under what conditions?

**Starting point.** Szirmai and Verspagen (2015), "Manufacturing and economic growth in developing countries, 1950–2005" (L120), henceforth S&V.

---

## Part A. Literature

### A1. The paper to replicate: Szirmai and Verspagen (2015)

*Read in its published version (SCED 34: 46–59), verified (L120).*

- **Data.**
  - 88 countries (67 developing, 21 advanced), 1950–2005, in eleven five-year periods.
  - Sector shares are value-added shares of GDP at current prices: World Bank WDI, filled for early years from UN national accounts, GGDC and UNIDO data.
  - Growth of GDP per capita from Maddison.
  - Education: average years of schooling, population 15 and over (Barro–Lee 2010, gaps filled from other sources).
  - Controls: income relative to the US (a ratio, not logged), log population, openness (trade/GDP, PWT 6.3), and a temperate-climate dummy (Gallup et al. 1999).
- **Specification.** Growth over a five-year period is regressed on values at the start of the period, with period dummies:

  > g(i, t→t+5) = α·MAN + β·RELUS + γ·EDU + [δ·MAN×RELUS + φ·MAN×EDU] + SER + ln POP + OPEN + TEMPERATE + period dummies

  The bracketed interactions are added in the second model.
- **Estimators.** Random and fixed effects, between, and **Hausman–Taylor** (the main one). MAN, SER, RELUS, EDU and the interactions are treated as endogenous; population and openness as exogenous; the climate dummy as the time-invariant instrument.
- **Subperiods.** 1950–70, 1970–90 and 1990–2005, implemented as slope shifts within one regression.
- **Findings.**
  - A 10-point higher manufacturing share goes with about 0.5 points faster growth (HT 0.045). Services have no effect.
  - With interactions, manufacturing helps more the poorer the country relative to the US and the more educated its population (MAN×RELUS −0.24, MAN×EDU +0.027, Table 3 col. 3). The education effect itself turns positive only above a manufacturing share of about 24%.
  - By subperiod, the direct effect is significant only in 1970–90. After 1990 the education threshold rises and the catch-up bonus shrinks: manufacturing became "a harder road".
- **Gaps for replication.**
  - No country list.
  - Observation counts that do not reconcile (790 vs 922–954).
  - SER appears in the tables but not the equations.
  - Hausman–Taylor standard errors not described.
  - Thresholds read from figures.

  The replication target is therefore **signs, rough magnitudes and significance patterns**, not exact digits.

The earlier companion, Szirmai (2012, L121), reached the same view with more emphasis on mixed statistical evidence: manufacturing matters, but not every prediction of the engine-of-growth hypothesis holds, and the historical record supports it more strongly than the regressions.

### A2. Is manufacturing still special? Evidence since S&V

- **Manufacturing remains an engine, conditionally.**
  - Haraguchi, Cheng and Smeets (2017, L122): manufacturing's share of *world* value added and employment has been roughly stable since 1970. Declines in many developing countries reflect concentration in a few populous economies, not a loss of potential.
  - Su and Yao (2017, L126): in middle-income economies manufacturing growth pulls along other sectors and is associated with higher saving and faster technology accumulation.
  - Marconi, Reis and Araujo (2016, L125): Kaldor's first and second laws hold in 63 middle- and high-income countries over 1990–2011, most strongly in middle-income ones.
  - Cantore et al. (2017, L124): in 80 countries over 1980–2010, using GMM, manufacturing growth helps when it comes from productivity and from a rising manufacturing share of jobs, not from employment scale.
- **Unconditional convergence.**
  - Rodrik (2013, L020): formal manufacturing converges unconditionally to the frontier at about 2–3% a year, though economies as a whole do not.
  - Kinfemichael and Morshed (2019, L127) report unconditional convergence in services too, and argue it now drives aggregate convergence. This questions manufacturing's uniqueness.
- **The path has narrowed.**
  - Rodrik (2016, L021): peak manufacturing shares come at lower incomes; Latin America has been hit hardest.
  - Felipe, Mehta and Rhee (2019, L067): almost every rich economy once had a manufacturing *employment* share of 18–20%, but the attainable peak has fallen to 13–15%. Employment shares predict prosperity better than output shares.
  - Kruse et al. (2022, L115): using the ETD, they find a "manufacturing renaissance" in several middle-income and low-income Asian and African countries since the 2000s, much of it in unregistered firms in Africa.

### A3. Services as alternative motors

- **Heterogeneity is the consensus.**
  - Di Meglio et al. (2018, L123): in 29 developing economies over 1975–2005, business services behave like manufacturing in Kaldorian tests; other services slow aggregate growth.
  - Nayyar, Hallward-Driemeier and Davies (2021, L056): ICT, professional and other tradable services offer scale, innovation and spillovers; low-skill services absorb labour with little productivity growth.
  - Rodrik and Sandhu (2024, L049): upgrading labour-absorbing services is unavoidable, because manufacturing cannot absorb the urban labour force.
- **Productivity growth in consumer services can drive transformation, but the gains are unequal.** Fan, Peters and Zilibotti (2023, L128) find this for India, 1987–2011, with gains skewed to high-income urban households.
- **Tourism in the Caribbean.** Cannonier and Burke (2019, L131) find a positive, significant effect of tourism spending on growth in Caribbean small island states. Tourism is the obvious candidate "services motor" there.

### A4. Latin America specifically

- Palma (2019, L130): Latin American productivity grew about 2.8% a year in 1950–80 and about 0.2% a year after 1980. He calls the region's manufacturing experience "non-creative destruction", with a Dutch-disease component, in contrast to Asia's use of reforms to deepen industrialisation.
- Rodrik (2016, L021): the region's deindustrialisation is especially premature.
- This project:
  - WP06: since 2000 the region's productivity problem has been within sectors, and manufacturing lost employment share while staying above average productivity.
  - Strand 3 of the literature review (`docs/literature/03_industrialization_and_services.md`): manufacturing's value came from a bundle of properties that has since come apart.

### A5. What the literature leaves open, and where this paper can add

1. **No update of S&V past 2005.** The literature since has used different specifications (Kaldor laws, GMM on growth rates, convergence), so none answers whether *S&V's own result* survived 2005–2023, the China-shock and post-boom years.
2. **LAC is folded into "developing countries".** No study asks whether the manufacturing effect was ever positive for Latin American and Caribbean countries specifically, including the import-substitution decades before 1980.
3. **Conditions are tested one at a time.** S&V tested education and the income gap. Others suggest export orientation, country size, commodity dependence, the real exchange rate and the global period. A joint, pre-specified test is missing.
4. **Services are tested either too coarsely or in small samples.** S&V used total services; Di Meglio et al. used 29 countries to 2005. The ETD now allows a 12-sector test for 51 countries to 2018.
5. **Robustness is reported selectively.** A full specification curve over estimators, samples, period lengths and share measures would show how much each conclusion depends on choices.

---

## Part B. Pre-analysis plan

### B1. Data (all committed in `empirics/data/source/`)

| Variable | S&V | Here | Note |
|---|---|---|---|
| Growth of GDP per capita (dependent) | Maddison | PWT 11.0 `rgdpna/pop` (national-accounts growth) | Maddison not in hand; PWT's national-accounts series is the closest equivalent |
| Income relative to the US (RELUS) | Maddison | PWT `rgdpo/pop` relative to the USA | Ratio, as in S&V |
| Manufacturing and sector shares, current prices | WDI plus fills | UN AMA (1970–2024, 220 countries); GGDC 10-Sector before 1970 (30 countries) | Same concept (value-added share at current prices); WDI is itself built from UN data |
| Education, 15+ | Barro–Lee 2010 | Barro–Lee v2.2 (1950–2010); PWT human-capital index `hc` after 2010 | `hc` extends Barro–Lee; switch documented and tested where both exist |
| Population | UN | PWT `pop` | |
| Openness | PWT 6.3 | UN AMA exports + imports / GDP; PWT `csh_x`, `csh_m` as check | |
| Temperate climate (time-invariant instrument) | Gallup et al. 1999 | **Not in hand** (OQ-48) | Needed for Hausman–Taylor |
| Finer sectors | — | ETD (12 sectors, 51 countries, 1990–2018) | Services split: trade, transport, business, finance, real estate, government, other |
| Employment shares | — | ETD, GGDC 10-Sector, ILO | For the Felipe et al. test |

### B2. Step 1: replicate S&V (1950–2005)

- Same sample frame (countries with data), same five-year periods, same regressors at period start, same estimators: RE, FE, BE and Hausman–Taylor.
- Hausman–Taylor has no standard Python implementation. It will be coded from the textbook GLS-IV formulas and **validated against a published worked example before use** (OQ-49).
- **Success criterion:** MAN positive and significant in the pooled HT model; MAN×RELUS negative and MAN×EDU positive; a stronger 1970–90 effect than 1990–2005.
- **Partial replication:** same signs, different significance. **Failure:** a different sign.
- Any of these is reported. A failure is diagnosed by moving one data source at a time back towards S&V's: period, sample, growth source, education source.

### B3. Step 2: is manufacturing still a motor? (Question 1)

- Extend the panel to 2005–10, 2010–15 and 2015–20, plus 2020–23 as a short final period, flagged.
- **Tests.** The MAN coefficient and the marginal-effect surface (MAN × education × income gap) by subperiod: 1970–90, 1990–2005, 2005–20. Rolling 20-year windows show when any change happened.
- **Reading.**
  - *Still a motor*: the marginal effect of MAN is positive and significant for 2005–20 at the median developing country's education and income gap.
  - *No longer a motor*: it is not distinguishable from zero across the whole relevant range.
  - *Narrower*: positive only above an education or income threshold that has risen since 1990.

### B4. Step 3: was it ever a motor in LAC? (Question 2)

- Add LAC × MAN slope shifts by subperiod, including 1950–70 (GGDC 10-Sector countries: Argentina, Bolivia, Brazil, Chile, Colombia, Costa Rica, Mexico, Peru, Venezuela).
- **Reading.**
  - *Yes, during import substitution*: a positive LAC manufacturing effect before 1980.
  - *No*: never distinguishable from the rest of the developing world, or below it.
  - *The engine stalled*: a positive effect that disappears after 1980.
- **Complement: Kaldor's first law.** The relation between manufacturing output growth and GDP growth, by LAC country and decade, using the GGDC 10-Sector and UN data.

### B5. Step 4: why only in some contexts? (Question 3)

Pre-specified moderators, each interacted with MAN. Each comes with the mechanism it stands for and the sign the mechanism predicts:

| Moderator | Mechanism | Predicted sign |
|---|---|---|
| Education (S&V) | absorptive capacity | + |
| Income gap (S&V) | room to catch up | + |
| Openness | export markets remove the demand ceiling | + |
| Population | home-market scale | + |
| Commodity dependence: mining share of value added | Dutch disease, crowding out | − |
| Real-exchange-rate undervaluation (Rodrik's index from PWT price levels) | profitability of tradables | + |
| Post-2001 period | competition from China | − |

- Estimated one at a time, then jointly with the S&V pair.
- **Supported** if the sign holds and is robust across the specification curve.
- **Rejected** if the sign is wrong or depends on specification.

### B6. Step 5: other candidate motors (Question 4)

Each candidate is run through the same specification:

1. **UN AMA groups**, all countries 1970–2024: construction; trade, restaurants and hotels; transport, storage and communication; other activities; mining and utilities.
2. **ETD, 12 sectors**, 51 countries 1990–2018: business services, financial services, trade, transport, real estate and government services, entered one at a time and with manufacturing.
3. **Employment instead of output shares** for manufacturing and each services group (Felipe et al.).
4. **Caribbean tourism.** Data on tourism value added are not in hand. Trade, restaurants and hotels serves as a proxy, flagged as weak (OQ-50).

**Reading.** A sector is a *motor* if its share predicts faster subsequent growth with the same robustness as manufacturing. It is *conditional* if it predicts growth only under identifiable conditions (B5's moderators). It is *not a motor* otherwise. Business services and tourism are the leading candidates (A3).

### B7. Robustness (specification curve)

The dashboard will show every combination of the following, each estimate classified as robustly positive, robustly negative or fragile, as in WP06:
- **Estimator:** RE, FE, HT, system GMM.
- **Period length:** 5 or 10 years.
- **Sample:** all, developing only, excluding oil exporters, excluding small states.
- **Share measure:** current or constant prices; output or employment.
- **Growth source:** PWT `rgdpna` or `rgdpo`.

### B8. What this design cannot do

- **No causal identification.** Initial-period shares and Hausman–Taylor reduce, but do not remove, reverse causality and omitted variables. S&V say the same.
- **Not about segments.** "Manufacturing" here is a sector. Its formal and informal segments (P1) cannot be separated with these data.
- **Weaker before 1970.** Coverage before 1970 is limited to 30 countries, so results for 1950–70 rest on a smaller, selected sample.

### B9. Outputs

- **Code:** `empirics/code/motors/` (steps 01–07, `run_all.py`, `tests/`).
- **Tables and figures:** `empirics/output/motors/`.
- **Dashboard:** `apps/motors/`, organised by the four questions, with a robustness page and a data page.
- **Paper:** `papers/WP07_development_motors/`.

---

## References (register IDs)

L003 Kaldor (1966) · L020 Rodrik (2013) · L021 Rodrik (2016) · L049 Rodrik & Sandhu (2024) · L056 Nayyar, Hallward-Driemeier & Davies (2021) · L067 Felipe, Mehta & Rhee (2019) · L115 Kruse et al. (2022) · L120 Szirmai & Verspagen (2015) · L121 Szirmai (2012) · L122 Haraguchi, Cheng & Smeets (2017) · L123 Di Meglio, Gallego, Maroto & Savona (2018) · L124 Cantore, Clara, Lavopa & Soare (2017) · L125 Marconi, Reis & Araujo (2016) · L126 Su & Yao (2017) · L127 Kinfemichael & Morshed (2019) · L128 Fan, Peters & Zilibotti (2023) · L129 Feenstra, Inklaar & Timmer (2015), PWT · L130 Palma (2019) · L131 Cannonier & Burke (2019) · L132 de Vries et al. (2021), ETD · L133 Timmer, de Vries & de Vries (2015), GGDC 10-Sector · L134 Barro & Lee (2013)
