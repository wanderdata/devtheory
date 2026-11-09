# WP07 — Development Motors: Is Manufacturing Still the Engine of Growth? An Update of Szirmai and Verspagen (2015)

*Paul Wander. Draft v0.1, 2026-11-09.*

**Plan written before estimation:** [00_literature_and_plan.md](00_literature_and_plan.md) (D-037) · **Code:** [`empirics/code/motors/`](../../empirics/code/motors/) (`run_all.py`) · **Generated outputs:** [`empirics/output/motors/`](../../empirics/output/motors/) · **Dashboard:** [`apps/motors/`](../../apps/motors/README.md) · **Decisions:** D-037 to D-040

## Summary

Szirmai and Verspagen (2015; "S&V") found that in 88 countries over 1950–2005, a larger manufacturing share of GDP predicted faster growth. The effect was larger where schooling was higher and the gap to the United States wider, and manufacturing became "a harder road" after 1990. This paper replicates their test, extends it to 2020 for up to 132 countries, and asks four questions. The tests and the readings that would count as support or rejection were fixed before estimation.

1. **Is manufacturing still a motor?** Not in the sense S&V tested.
   - Since 1990 a larger initial manufacturing share has predicted *slower* growth at a given income and schooling. That is robust across 192 specifications for 1990–2005 (median −0.13 pp of annual growth per point of share) and leaning negative for 2005–20 (median −0.07).
   - For 1970–90 the estimate is positive when manufacturing is tested on its own (median +0.07, leaning positive), but fragile once the services share is also controlled for.
2. **Was it ever a motor in Latin America and the Caribbean?** Not distinguishably from elsewhere.
   - The LAC slope never differs robustly from the rest of the world's, including in 1950–70, the import-substitution years.
   - After 1990 the LAC slope is, if anything, less negative.
   - Manufacturing and GDP growth moved closely together in the region in every decade (Kaldor's first law), in its booms and its busts alike.
3. **Why only in some contexts?** The conditions S&V found are fragile.
   - Their two interactions replicate almost exactly once former planned economies are excluded: manufacturing × income gap −0.240 against their −0.241, manufacturing × schooling +0.038 against +0.027.
   - The income-gap interaction depends on 13 observations from three Gulf oil states. When commodity exporters are also excluded, it reverses sign.
   - Among further conditions, schooling and a post-2000 penalty hold in that core sample, country size in the main sample. Currency undervaluation strongly raises manufacturing's payoff in the core sample but has the opposite sign in the main sample. Openness and commodity dependence show nothing.
4. **Do other sectors act as motors?** No sector's output share robustly predicts faster growth after 2005, except agriculture's, which most plausibly measures room to move workers out of farming.
   - Services as a whole, and finance, business, government and personal services together, are robustly associated with *slower* growth after 2005.
   - In the 12-sector ETD data (50 developing and emerging economies, 1990–2020), business and financial services, the candidates most often proposed as new motors, are associated with slower growth by both output and employment share.
   - Manufacturing's *employment* share, unlike its output share, predicts faster growth there.

The results are conditional associations, not causal effects. In particular, a negative manufacturing coefficient does not show that manufacturing harms growth (§6).

## 1. Question and approach

The engine-of-growth hypothesis (Kaldor 1966, L003) holds that manufacturing drives development through increasing returns, learning and tradability. The evidence for developing countries rests heavily on S&V (L120) and its companion (Szirmai 2012, L121). Since then the literature has moved to other designs:
- Kaldor-law regressions (Di Meglio et al. 2018, L123; Marconi et al. 2016, L125);
- GMM on growth rates (Cantore et al. 2017, L124);
- convergence tests (Rodrik 2013, L020; Kinfemichael & Morshed 2019, L127);
- world shares (Haraguchi et al. 2017, L122).

None has asked whether S&V's own result survives the period since 2005. None has asked whether it ever held for Latin America and the Caribbean specifically. None has tested services in the same frame with modern 12-sector data.

The approach is deliberately conservative. First replicate S&V with sources as close to theirs as are available (§3). Then change one thing at a time: the period (§4), the region (§5), the conditions, and the sector. Every headline estimate is classified by how it behaves across 192 combinations of analytical choices.

## 2. Data and specification

**Specification (S&V eq. 1–2).** The dependent variable is the average annual growth of GDP per head over a five-year period, 100 × (y₍ₜ₊₅₎/yₜ − 1)/5. The regressors, all measured at the start of the period, are:
- the manufacturing share of value added (current prices);
- the services share;
- GDP per head relative to the US (a ratio);
- average years of schooling of the population aged 15 and over;
- log population and openness;
- a temperate-climate dummy;
- period dummies;
- and, in the extended model, manufacturing × relative income and manufacturing × schooling.

The main estimator is **Hausman–Taylor**, with the shares, relative income, schooling and interactions treated as endogenous, and population, openness and the period dummies as exogenous. The implementation was written for this project and reproduces the published estimates for the standard textbook example (Cornwell–Rupert wage panel) to within 0.00005 on all thirteen coefficients (OQ-49, closed). Fixed and random effects with country-clustered errors are reported alongside.

**Sources and differences from S&V (D-037, D-038).**

| Variable | S&V | Here |
|---|---|---|
| Growth, income gap | Maddison | Penn World Table 11.0 |
| Sector shares | WDI, with fills | UN national accounts from 1970; GGDC 10-Sector before 1970 (about 30 countries), ratio-spliced to the UN level in 1970 and rescaled to sum to 100 |
| Schooling | Barro–Lee 2010 | Replication: Barro–Lee v2.2 (to 2010). Extension: years implied by PWT's human-capital index (correlation with Barro–Lee 0.97) |
| Temperate climate | share of land in the temperate zone (Gallup et al.) | dummy for a centroid outside the tropics (OQ-48, closed by substitution) |
| Finer sectors | — | ETD, 12 sectors, value added and employment, 1990–2018 |

**Samples (D-037, D-039).**
- *Main* (pre-specified): countries with at least 1 million people in 2000.
- *Excluding former planned economies*: shares measured at planned prices are not comparable, and S&V note these economies are under-represented in their data.
- *Core*: also excludes commodity exporters, defined as mining and utilities above 20% of value added on average.
- *Developing*: core without the 21 long-standing OECD economies.

The last three were added after the replication showed that results depend on them (§3). They are reported as such, not substituted for the pre-specified sample.

## 3. Replication (1950–2005)

The main sample has 858 country-periods in 125 countries, against S&V's 790 in 88.

**The unconditional manufacturing effect does not replicate.** S&V's Hausman–Taylor estimate is +0.045: a 10-point larger share goes with 0.45 points faster growth. Here it is:

| Sample | Hausman–Taylor | p |
|---|---|---|
| Main | −0.047 | 0.23 |
| Excluding former planned economies | −0.007 | 0.86 |
| Core | −0.043 | 0.25 |

Fixed effects, random effects and between estimates are equally close to zero in every sample. The negative relation with relative income (catch-up) does replicate everywhere.

**The interactions replicate closely, in the right sample.** Without former planned economies, the full interaction model gives manufacturing × relative income −0.240 (S&V −0.241) and manufacturing × schooling +0.038 (S&V +0.027), both significant at 1%. With separate slopes for 1950–70, 1970–90 and 1990–2005, all six interaction terms match S&V in sign and significance (S&V Table 4, model 3). In the main sample the income interaction replicates; the schooling interaction has the right sign but is not significant.

**But they rest on a handful of oil states.** In the main sample, the income-gap interaction is identified largely by 13 observations of three Gulf economies, the UAE, Kuwait and Saudi Arabia, recorded by PWT at 1.6 to 9.8 times US income per head between 1970 and 2000. These countries combined very high measured income with slow or negative growth and small manufacturing shares. Excluding commodity exporters reverses the interaction: in the core sample it is +0.367 (p = 0.03), and the schooling interaction disappears (−0.013, p = 0.42). Fixed and random effects give the same pattern, so the estimator is not responsible.

S&V's sample of 88 countries probably excluded these economies, but their country list is not published, so this cannot be confirmed. **Read with the oil states, the S&V result says manufacturing paid off more the poorer the country. Read without them, the opposite.**

## 4. Is manufacturing still a motor? (Question 1)

The panel is extended to 2015–20, with schooling from PWT's human-capital index to keep a consistent series. One regression with a separate manufacturing slope per subperiod (main sample, 1,295 observations, 132 countries; Hausman–Taylor) gives:

| Subperiod | Main sample | Core sample |
|---|---|---|
| 1950–70 | −0.014 | −0.023 |
| 1970–90 | +0.056 (p = 0.08) | +0.078 (p = 0.01) |
| 1990–2005 | −0.117 (p < 0.01) | −0.081 (p = 0.03) |
| 2005–20 | −0.047 (p = 0.22) | −0.042 (p = 0.28) |

Twenty-year rolling windows show the turn plainly. The slope is close to zero or slightly positive for windows centred on the 1970s, then falls to about −0.2 for windows covering 1980–2010. It recovers only partly after that.

With the S&V interactions, the marginal effect of manufacturing at the median developing country's income gap and schooling in each subperiod is:
- about zero in 1970–90;
- significantly negative in 1990–2005 (−0.136 in the main sample, −0.157 core);
- zero in 2005–20 in the main sample, negative in the core sample (−0.110, p = 0.01).

**Across 192 specifications:**

| Estimate | Verdict | Median |
|---|---|---|
| 1990–2005 slope | robustly negative | −0.134 |
| 2005–20 slope | leaning negative | −0.067 |
| 1970–90 slope, with services share also included | fragile | +0.012 |
| 1970–90 slope, manufacturing alone | leaning positive | +0.068 |

**Reading against the plan (B3).** The "still a motor" reading would require a positive, significant effect at the median developing country in 2005–20. That is rejected. The "no longer a motor" reading, no effect across the relevant range, fits 2005–20. For 1990–2005 the data go further than the plan anticipated: the association is negative. This sharpens S&V's "harder road after 1990". It is not a narrowed road but one that, in this test, no longer shows up at all.

## 5. Was manufacturing ever a motor in Latin America and the Caribbean? (Question 2)

**S&V test with separate slopes.** With separate manufacturing slopes for LAC and the rest of the world in each subperiod (8 LAC countries in 1950–70, 21 after; main sample, Hausman–Taylor):

| Subperiod | LAC | Rest of the world | p of difference |
|---|---|---|---|
| 1950–70 | +0.038 | −0.040 | 0.31 |
| 1970–90 | +0.083 | +0.061 | 0.70 |
| 1990–2005 | −0.034 | −0.129 | 0.13 |
| 2005–20 | +0.008 | −0.053 | 0.44 |

The core sample shows no difference in any period. With fixed effects in the main sample, LAC's slope is significantly higher after 1990, meaning less negative. Across 192 specifications the LAC difference is *fragile* for 1970–90 and 2005–20 and *leaning positive* for 1990–2005. The LAC slope itself is never robustly positive, including in 1950–70.

**Kaldor's first law.** Cross-country slopes of GDP growth on manufacturing growth, by decade, are 0.37 to 0.74 in LAC. They are steeper than in the rest of the world in the 1960s, 1970s, 1980s and 2010s. Manufacturing's share of GDP was around 0.15–0.30, so slopes this high are what Kaldor's argument predicts. But the steepest LAC slopes come in the debt-crisis 1980s (0.74) and the stagnant 2010s (0.66). Manufacturing and GDP growth moved together in LAC in falls as much as in rises. The law describes how tightly the region's growth was tied to its manufacturing; it does not show that manufacturing drove it.

**Reading against the plan (B4).**
- *"Yes, during import substitution"* (a positive LAC effect before 1980): not supported. The 1950–70 estimate rests on eight countries and is imprecise.
- *"The engine stalled"* (positive, then gone): only weakly consistent. The 1970–90 point estimate is positive and the post-1990 one is not, but neither is distinguishable from the rest of the world.
- **Best supported:** manufacturing never worked as a distinctively LAC motor in this test. Its decline after 1990 cost LAC no more than other regions.

This bears on Palma's (2019, L130) reading of the region's "non-creative destruction" of manufacturing. The destruction is visible in the shares, but these data do not show that a larger share would have bought faster growth after 1990.

## 6. Why only in some contexts? (Question 3)

Each pre-specified condition is interacted with the manufacturing share, one at a time, centred at the median developing country (1950–2020). A condition counts as **supported** in a sample if Hausman–Taylor and fixed effects both give the predicted sign and at least one is significant at 10%.

| Condition (mechanism) | Predicted | Main sample | Core sample | Verdict |
|---|---|---|---|---|
| Schooling (absorptive capacity) | + | + (n.s.) | + (HT p = 0.03) | supported in core only |
| Income relative to US (catch-up) | − | − (HT p = 0.03) | **+** (p < 0.01) | conflicting |
| Openness (export markets) | + | 0 | 0 | no evidence |
| Population (home market) | + | + (p < 0.03) | + (n.s.) | supported in main only |
| Mining & utilities share (Dutch disease) | − | 0 | 0 | no evidence |
| Currency undervaluation (tradables' profitability) | + | **−** (HT p = 0.04) | + (p < 0.03) | conflicting |
| From 2000 (competition from China) | − | 0 | − (HT p = 0.045) | supported in core only |

The answer to "why only in some contexts" is therefore less tidy than S&V's.

- In the core sample, which drops former planned and commodity economies, manufacturing pays off more:
  - where schooling is higher;
  - where the currency is undervalued, consistent with Rodrik's argument that undervaluation favours tradables;
  - before 2000 rather than after, consistent with competition from China.
- In that sample, manufacturing paid off *more*, not less, the closer the country was to US income. This contradicts S&V's catch-up reading.
- In the main sample, the oil and planned economies dominate the income-gap and price-level variation, and the signs change.

What makes manufacturing work cannot be separated from which economies are compared. The core sample is the cleaner comparison, but it was chosen after seeing the replication (D-039).

## 7. Other candidate motors (Question 4)

**UN sector groups, 1970–2020.** Each sector's share is tested on its own in the same specification. Across 96 specifications per sector:

| Sector | 1970–90 | 1990–2005 | 2005–20 |
|---|---|---|---|
| Manufacturing | leaning + | robustly − | leaning − |
| Trade, restaurants & hotels | robustly + | fragile | fragile |
| Transport, storage & communications | leaning + | fragile | fragile |
| Other services (finance, business, government, personal) | leaning + | leaning − | robustly − |
| All services | leaning + | leaning − | robustly − |
| Construction | leaning + | leaning − | fragile |
| Agriculture | fragile | leaning + | robustly + |
| Mining & utilities | leaning − | fragile | fragile |

Before 1990, most sector shares other than mining had positive slopes: an economy with less mining and agriculture grew faster. After 1990 the only robust positive is agriculture. That is almost certainly not agriculture as a motor. At a given income and schooling, a larger farm share means more room to raise productivity by moving workers out, the static reallocation gain documented in WP06.

**ETD, 12 sectors, 1990–2020** (up to 50 countries, 297 country-periods; Hausman–Taylor, main sample). Verdicts are robust across samples and estimators unless stated.

| Sector | Value-added share | Employment share |
|---|---|---|
| Manufacturing | −0.031 (no effect) | **+0.123 (p = 0.01; motor)** |
| Business services | **−0.276 (p < 0.01; drag)** | **−0.552 (p < 0.01; drag)** |
| Financial services | **−0.221 (p = 0.05; drag)** | **−0.673 (p = 0.03; drag)** |
| Trade services | +0.241 (p < 0.01; motor) | −0.009 (no effect) |
| Construction | +0.125 (p = 0.08; motor) | no effect |
| Real estate | +0.170 (motor) | −1.029 (drag) |
| Transport, government, other services, agriculture, mining, utilities | no effect | no effect |

Three readings follow.

1. **Jobs, not output.** Manufacturing's employment share predicts growth; its output share does not. This is Felipe, Mehta and Rhee's (2019, L067) "it's the jobs that count", here in a 1990–2020 panel. It is also consistent with Cantore et al. (2017, L124): manufacturing helps when it raises its share of employment, not through scale alone.
2. **The services usually proposed as new motors do not behave like one in this test.** Business and financial services shares, at a given income and schooling, go with slower subsequent growth. This contrasts with Di Meglio et al. (2018, L123), who found business services supported growth in 29 economies over 1975–2005, and with the optimism of Nayyar et al. (2021, L056). A likely reading is that a large modern-services share in a developing economy at a given income often marks early deindustrialisation and financialisation rather than a new engine. The test cannot distinguish that from reverse causation.
3. **Trade services and construction** are associated with faster growth by output share in the ETD sample. That is consistent with Fan, Peters and Zilibotti's (2023, L128) finding that productivity growth in consumer services mattered in India. The trade result is not robust in the longer UN sample after 1990.

**The Caribbean.** With no tourism value-added series in hand (OQ-50), trade, restaurants and hotels is used as a proxy, with a separate slope for the Caribbean (all countries regardless of size, 1970–2020). The Caribbean slope is −0.26 (Hausman–Taylor, p = 0.07; fixed effects −0.28, p = 0.18), on only seven Caribbean countries with complete data. That is no support for tourism-led growth here, but on a weak proxy and a small sample. Cannonier and Burke (2019, L131) find the opposite using tourism spending.

## 8. What the evidence shows, what it does not, and what would change it

**What it shows.**
- The specific regularity S&V documented — a larger initial manufacturing share predicting faster growth — does not hold in data extended to 2020 and with more countries. It is absent or negative after 1990.
- The conditions under which it held depend on which economies are compared, especially oil exporters.
- No other sector's share has taken manufacturing's place in this test.
- Manufacturing's employment share retains predictive power that its output share has lost.

**What it does not show.**
- *That manufacturing harms growth.* The estimates are conditional associations. Hausman–Taylor and fixed effects remove permanent country differences, but not shocks that move growth and shares together. The obvious one is a commodity boom, which raises growth and shrinks manufacturing's share. Commodity price swings (the slump of the 1990s, the boom from about 2003) would produce negative within-country associations of exactly this kind. Excluding commodity exporters (the core sample) weakens but does not remove the negative association.
- *That manufacturing no longer matters.* "Motor" here means a larger share predicts faster growth over the next five years. Manufacturing's contribution through learning, exports, linkages and good jobs may work over longer horizons or through employment rather than output. The employment-share result points in that direction.
- *Anything about segments.* Formal and informal manufacturing or services cannot be separated with these data (P1, P2).

**What would change the conclusions.**
- A causal design: instruments for manufacturing shares such as external demand or exchange-rate shocks, or a GMM estimator validated like the HT implementation here (D-040).
- S&V's own country list, which would show whether their positive unconditional effect reflects their sample.
- Tourism data for the Caribbean (OQ-50).

## 9. Departures from the pre-analysis plan

1. **Samples (D-039).** The *excluding planned* and *core* samples were added after the replication. Verdicts require agreement between the main and core samples, so the post-hoc sample cannot by itself produce a finding.
2. **System GMM (D-040).** Listed in the plan's specification curve, it was dropped: no implementation could be validated here, and an unvalidated GMM would add noise, not robustness.
3. **The climate instrument.** S&V's temperate-land share was replaced by a centroid-latitude dummy (OQ-48).
4. **The Caribbean tourism test** uses a proxy, as the plan anticipated.

## References

Register IDs; see `references/literature_register.csv` for status (most post-2015 papers were checked against abstracts only).

L003 Kaldor (1966) · L020 Rodrik (2013) · L021 Rodrik (2016) · L049 Rodrik & Sandhu (2024) · L056 Nayyar, Hallward-Driemeier & Davies (2021) · L067 Felipe, Mehta & Rhee (2019) · L115 Kruse et al. (2022) · L120 Szirmai & Verspagen (2015) · L121 Szirmai (2012) · L122 Haraguchi, Cheng & Smeets (2017) · L123 Di Meglio et al. (2018) · L124 Cantore et al. (2017) · L125 Marconi, Reis & Araujo (2016) · L126 Su & Yao (2017) · L127 Kinfemichael & Morshed (2019) · L128 Fan, Peters & Zilibotti (2023) · L129 PWT 11.0 · L130 Palma (2019) · L131 Cannonier & Burke (2019) · L132 ETD · L133 GGDC 10-Sector · L134 Barro & Lee (2013)
