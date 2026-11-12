# WP08 — Defining and Measuring Productive Development: The Working-Age Population on a Productivity Ladder

*Paul Wander. Draft v0.1, 2026-11-12.*

**Concept note:** [`docs/theory/03_defining_productive_development.md`](../../docs/theory/03_defining_productive_development.md) · **Code:** [`empirics/code/lp/08_ladder.py`, `09_baumol.py`](../../empirics/code/lp/README.md) · **Generated outputs:** [LAC ladder results](../../empirics/output/lac_lp/ladder/results.md), [LAC relative prices](../../empirics/output/lac_lp/baumol/results.md), [Caribbean ladder results](../../empirics/output/carib_lp/ladder/results.md), [Caribbean relative prices](../../empirics/output/carib_lp/baumol/results.md) · **Dashboard:** [`apps/productivity/`](../../apps/productivity/README.md), pages *Output per working-age person* and *Ladder of the working-age population* · **Decisions:** D-042 to D-044 · **Propositions:** P25–P27

## Summary

This paper proposes a definition of productive development and applies it to 29 Latin American and Caribbean economies, 1991–2024.

**The definition.** Productive development is a sustained improvement in the distribution of the working-age population across the productivity of the work they do, with people not in work counted at zero. The mean of this distribution is output per working-age person. Its lower part measures structural heterogeneity. A change is judged by whether the later distribution dominates the earlier one, at two price bases.

The findings, each qualified in the text:

1. **The employment rate matters in the short run and much less in the long run.** Productivity and the employment rate have opposite signs in 41–50% of windows, whatever the length of the window. But the employment-rate term's share of the variance of growth of output per working-age person falls from 27% over one-year windows to 8% over twenty-year windows. The dispute between a productivity-only definition and an output-per-working-age-person definition is mostly about short horizons.
2. **Over 2000–19, productivity within sectors accounts for most growth of output per working-age person.** The median well-anchored country (excluding Cuba and Venezuela) grew 1.63 log points a year. Of this, within-sector productivity accounts for 1.36, structural change for 0.15 and the employment rate for 0.25.
3. **The mean and the distribution often disagree.** Of 23 well-anchored countries over 2000–19, 7 show an unambiguous improvement (first-order dominance at both price bases). Another 5 improve when lower percentiles are given more weight. In 9 the ladders cross and the verdict is ambiguous: Brazil, Guatemala and Honduras among them, although their means rose. Over 2008–19 no well-anchored country shows an unambiguous improvement.
4. **Relative prices offset between a quarter and a half of the differences in real productivity growth between sectors.** A sector whose real productivity grew 1 point a year faster than the average saw its relative price fall by 0.27–0.48 points a year, depending on the period (−0.48 for 2000–19, 90% interval −0.62 to −0.29). In construction and in trade, restaurants and hotels, rising relative prices hide part of a fall in real relative productivity when productivity is measured at current prices.

The ladder in this paper has one step per sector, so it understates dispersion and treats every worker in a sector alike. The verdicts are about sector averages. Splitting sectors by formality and firm size is the next step (P26, OQ-57).

## 1. The question

Policy documents in the region use productive development to mean, at a minimum, rising productivity. One recent discussion asked whether the definition should also include employment, so that a country where productivity rises while output per person falls is not described as developing productively. There are two positions:

- **Productivity alone.** Its defenders argue that productivity is the source of sustained growth. A definition that penalised labour-saving productivity gains would rule out desirable changes. Short-run episodes in which productivity and output move apart, such as the 2020 rise in measured productivity as low-productivity workers lost their jobs, are exceptions to be explained.
- **Productivity plus employment.** The alternative uses growth of output per working-age person (GDP per capita net of demographics), which adds the employment rate to productivity. Its defenders point out that the two move in opposite directions often, so the choice of definition changes the diagnosis.

Each position is right about something. The first is right that productivity carries growth over long horizons, because the employment rate is bounded. The second is right that the employment rate is part of what people experience, and that its movements are frequent. Neither definition, however, says anything about the productive structure. Where the region's problem has been diagnosed, from Pinto onward, it has been in terms of structural heterogeneity: a large share of workers in low-productivity activities alongside a small, productive modern sector (L138). This paper proposes a definition that contains output per working-age person as a special case and also measures that heterogeneity.

## 2. Definition and measures

The full statement is in the concept note. Briefly:

- Each person aged 15 and over is placed at the productivity of the activity they work in, and everyone not employed is placed at zero. Sorted from lowest to highest, this gives a ladder. The width of each step is a share of the working-age population; its height is output per worker. The area under the ladder is output per working-age person.
- **Productive development** is a sustained improvement in this ladder that comes from the productive structure.
- **Judging a change.** A change is judged by first-order dominance (every percentile at least as high) and by second-order dominance (the cumulative area at least as high at every percentile). Both are required to hold at initial- and final-year prices. These tests come from the literature on poverty and income distribution (Atkinson 1987; Foster and Shorrocks 1988; L140–L141).
- **Supporting measures:**
  - the incidence curve, giving the change at each percentile (as in Ravallion and Chen 2003, L142);
  - the exact log decomposition of output per working-age person into within-sector productivity, structural change and the employment rate;
  - threshold indices below a productivity line (Foster, Greer and Thorbecke 1984, L143).

**Price windfalls.** At constant prices, a rise in export prices does not raise measured output. It does raise income, and that gain is reported separately as the terms-of-trade term.

## 3. Data and method

**Data.** The data are those of WP05 and WP06:
- UN National Accounts Main Aggregates (value added by seven sectors, current and constant 2020 US dollars; exports, imports and GDP for the terms-of-trade term);
- ILO modelled estimates of employment by sector and of the employment-to-population ratio for ages 15+, with the labour-force participation and unemployment rates to split the zero block.

The working-age population is ILO employment divided by the employment ratio, so that both refer to the same population (D-043). Total population for the demographic term is the ILO's series of UN estimates (D-044). The share of the 15+ population aged 65 and over, from the World Bank's WDI, is reported as context. The 29 countries with sector employment are covered. Grades A, B and C indicate whether the endpoints of a period are close to survey years (D-026).

**Periods and prices.** The fixed periods of WP06 are used: 1991–2000, 2000–08, 2008–19, 2019–24 and 2000–19. Each period is valued at its initial-year prices and, for the verdicts, also at its final-year prices (D-024, D-035).

**Decomposition.** The log growth of output per working-age person $Y/W$ is

$$\Delta \ln(Y/W) = \Delta \ln(Y/L) + \Delta \ln(L/W),$$

with $\Delta\ln(Y/L)$ divided between the within-sector and structural-change terms of the period decomposition in proportion to their linear values. The demographic term $\Delta\ln(W/N)$ and the terms-of-trade term are reported beside the sum. The terms-of-trade term is the growth of real gross domestic income over real GDP, with exports deflated by the import price deflator (OQ-62).

**Horizons.** For the horizon comparison, every window of 1, 5, 10 and 20 years between 1991 and 2024 is used, with official total value added at constant 2020 prices.

**Dominance.** On step functions, dominance can be checked exactly. First-order dominance compares the two cumulative distributions at every step value. Second-order dominance compares generalised Lorenz curves at every breakpoint of either ladder; both curves are linear between breakpoints. The functions are tested on constructed cases with known answers (`tests/test_ladder.py`).

**Relative prices.** For each sector, relative productivity at current prices is split exactly into a real part and a relative-price part:

$$\frac{p_i^{nom}}{P^{nom}} = \frac{p_i^{real}}{P^{real}} \times \frac{\pi_i}{\pi}$$

where $\pi_i$ and $\pi$ are implicit deflators. The cross-sector slope of the relative-price change on the real change is estimated by pooled OLS. Mining and utilities are excluded, because their prices follow world commodity prices. Countries are resampled for a 90% bootstrap interval.

## 4. Results

### 4.1 What drives output per working-age person, 2000–19

| Median, 22 countries graded A or B, excluding Cuba and Venezuela | Log points a year |
|---|---|
| Output per working-age person | +1.63 |
| Within-sector productivity | +1.36 |
| Structural change | +0.15 |
| Employment rate | +0.25 |
| *Beside the sum:* demographic term | +0.63 |
| *Beside the sum:* terms of trade | +0.03 |

- **The employment rate.** It rose in 16 of the 22 countries. It moved in the opposite direction to productivity in 9, and was the larger of the two in absolute value in one (Saint Lucia).
- **Falls in output per working-age person.** It fell in Mexico, the Bahamas, Belize and Jamaica.
- **Mexico.** Output per working-age person fell 0.22 log points a year. Within-sector productivity fell 0.46, offset in part by structural change (+0.15) and a slightly higher employment rate (+0.09).
- **The demographic dividend.** The working-age share of the population rose in every country (median +0.63 log points a year), so growth of output per person overstates growth of output per working-age person by about that much. The demographic term was larger than the employment-rate term in 16 of the 22 countries. The exceptions (Belize, Chile, the Dominican Republic, Panama, Peru and Uruguay) are the countries where the employment rate rose most.

### 4.2 Horizons (P25)

| LAC, all countries | 1 year | 5 years | 10 years | 20 years |
|---|---|---|---|---|
| Windows | 957 | 841 | 696 | 406 |
| Opposite signs | 0.50 | 0.46 | 0.48 | 0.41 |
| Employment-rate term larger | 0.34 | 0.27 | 0.24 | 0.13 |
| Its share of variance of growth of $Y/W$ | 0.27 | 0.13 | 0.12 | 0.08 |
| Productivity up while $Y/W$ fell | 0.060 | 0.052 | 0.042 | 0.017 |

**What the table shows.** Opposite signs are common at every horizon, so they are not an artefact of the cycle. But over long windows the employment-rate term is usually small. Over twenty-year windows its median absolute value is 0.30 log points a year, against 1.19 for productivity; over one-year windows the figures are 1.03 and 2.16. The case that motivated the debate, productivity rising while output per working-age person falls, occurs in 6% of one-year windows and 2% of twenty-year windows. Of the 57 one-year cases, 27 fall in 2020, 2009, 1998 and 1999.

**Excluding Cuba and Venezuela.** The pattern is the same, with a higher one-year variance share (0.32).

**Caribbean.** Most of the pattern holds, with one exception: over 20-year windows the employment-rate term is still the larger one in 22% of cases. Its variance share is 4%.

**Caveat.** The ILO's employment ratios are modelled, and in years far from a survey they are partly a model result. That applies most to the one-year figures for recent years.

### 4.3 Ladders and verdicts

| 2000–19, LAC, grades A and B (23 countries) | Countries |
|---|---|
| Improvement (first-order dominance at both price bases) | 7 |
| Improvement, weighting the lower percentiles | 5 |
| Ambiguous | 9 |
| Deterioration, weighting the lower percentiles | 1 |
| Depends on prices | 1 |

Over 2008–19 the corresponding counts (24 countries) are 0, 7, 12, 4 and 1. That is, no well-anchored country shows an unambiguous improvement over 2008–19, and four show a deterioration that weights the lower percentiles more.

Three cases illustrate what the verdicts add to the mean (2000–19, initial-year prices):

- **Chile (improvement).** Employment-rate and step changes worked together:
  - the share of the population aged 15+ not employed fell from 50.0% to 41.6%;
  - output per worker rose in every sector except construction, which fell from US$9.9k to 8.2k at 2000 prices.

  The quantile function rose at every percentile.
- **Brazil (ambiguous, mean up).** The mean rose 0.78% a year, but the ladders cross:
  - agriculture's output per worker more than doubled (US$3.1k to 7.2k) as its share of the population fell from 8.3% to 5.1%;
  - the zero block grew from 41.4% to 42.8%;
  - the trade, restaurants and hotels step widened from 12.4% to 14.3% while its height stayed at about US$3k per worker.

  Gains at the top and in agriculture coexist with losses at the bottom of the employed distribution.
- **Mexico (ambiguous, mean down).** The changes go in both directions:
  - the zero block shrank from 42.0% to 41.0%, and agriculture's output per worker rose;
  - trade, restaurants and hotels widened (13.7% to 16.0%) while its output per worker fell (US$17.8k to 14.6k);
  - manufacturing, construction and mining also fell.

  The bottom of the distribution improved slightly while the middle and the top fell.

**Uruguay.** Its verdict depends on prices. This is the telecoms case of WP06: the relative price of transport, storage and communication fell sharply, so the weight of that sector differs between the two bases.

**Caribbean.** Over 2000–19 the nine well-anchored Caribbean countries split into 2 improvements, 2 improvements weighting the lower percentiles and 5 ambiguous.

These verdicts treat everyone in a sector as equally productive. In Mexico and Brazil the trade sector is where informal employment is concentrated. A sector step that widens without rising may hide a growing informal segment and a stable formal one. Splitting the step could turn "ambiguous" into a clearer deterioration at the bottom (P26).

### 4.4 Terms of trade

The terms-of-trade term is small for the median country over 2000–19 (+0.03). It is large in sub-periods:
- in 2000–08 it added 1.2–1.4 points a year to real income in Bolivia, Ecuador and Chile, and 0.7 in Peru;
- over 2000–19 it added 0.75 in Chile.

This income does not appear in output at constant prices, and under D-042 it is not productive development. Reporting it beside the volume measure shows how much of the improvement in living standards during the commodity boom came from prices.

**Deflator.** The term deflates the trade balance by the import price deflator. With the average of the export and import deflators instead, the results are nearly the same: correlation 0.98–0.99 across country-periods, and a median absolute difference of 0.08 points a year for 2000–08 and 0.02–0.03 for the other periods. The sign changes in one country-period. The largest differences are for Venezuela (4.94 against 4.12 in 2000–08) and Ecuador (1.30 against 1.16) (OQ-62).

### 4.5 Relative prices and measured productivity (P27)

| LAC, excl. Cuba and Venezuela, mining and utilities excluded | Slope | 90% interval |
|---|---|---|
| 1991–2000 | −0.42 | [−0.64, −0.18] |
| 2000–08 | −0.38 | [−0.51, −0.23] |
| 2008–19 | −0.37 | [−0.54, −0.18] |
| 2019–24 | −0.27 | [−0.44, −0.18] |
| 2000–19 | −0.48 | [−0.62, −0.29] |

**The slope.** In every period the slope lies between −1 and 0 and its interval excludes both. Sectors with slower real productivity growth saw their relative prices rise, as Baumol's mechanism predicts (L144), but the rise offset between 27% and 48% of the difference, depending on the period.

**Caribbean.** The slopes are between −0.26 and −0.40.

**Low-productivity sectors, 2000–19.** For sectors whose output per worker at current prices was below the economy-wide average in 2000 (medians across countries):

| Sector | Countries | Relative productivity at current prices | Real part | Relative-price part |
|---|---|---|---|---|
| Construction | 19 | +0.25 | −0.80 | +0.59 |
| Trade, restaurants and hotels | 26 | −0.32 | −0.47 | +0.23 |
| Agriculture | 25 | +0.56 | +0.95 | −0.05 |

**Construction.** It looks better at current prices than it is in volume terms. Its relative productivity at current prices rose, while its real relative productivity fell by 0.8 points a year.

**Trade, restaurants and hotels.** Its real relative decline was partly hidden by a rising relative price.

**Agriculture.** Its relative gain was real.

**Measurement error.** Errors in sector employment bias the slope toward zero. Errors in sector deflators bias it toward −1. The estimates therefore cannot be read as a precise elasticity (OQ-59).

**Survey employment.** One check is possible on the employment side. Each grade-A country-period was recomputed between its two anchoring survey years, once with survey employment and once with ILO modelled employment. The relative-price term does not involve employment, so only the real term differs. For 2000–19 (15 countries) the slope is −0.30 with survey employment and −0.34 with modelled employment. For 2008–19 (17 countries) both are −0.38. The ILO's interpolation of employment does not drive the result. This sample's slope for 2000–19 is smaller in absolute value than the full sample's (−0.48), and the difference comes from the change of sample, not from the employment series. Errors in the sector deflators remain untested. The ETD's sector deflators for the nine Latin American countries it covers would allow a check.

**For the decomposition.** These results matter for any decomposition carried out at current prices or at the prices of a single year. Part of what looks like within-sector productivity growth in low-productivity services at current prices is a relative-price effect. The decompositions in WP05, WP06 and this paper use volumes valued at the prices of a given year, so they are not affected in the same way. Their sensitivity to the price base (D-035) is the same phenomenon seen from the other side.

### 4.6 Distance from the frontier

The verdicts compare each country with itself. Comparing countries needs a common line. Each sector's output per worker at constant 2020 prices is converted to 2020 US dollars at purchasing-power parity, with one price-level factor per country (PWT 11.0, `pl_gdpo` relative to the United States in 2020). It is then expressed as a share of US output per worker in the same year, computed from UN value added and ILO employment. The summary is the average gap below a line at 50% of US output per worker, over the whole population aged 15+, with the non-employed at zero (OQ-60).

| 27 countries with comparable levels | 2000 | 2019 |
|---|---|---|
| Median output per worker, % of US | 22.3 | 23.9 |
| Median average gap below 50% of US | 0.760 | 0.735 |

- **No general convergence.** The gap rose in 13 of the 27 countries, including Argentina, Brazil and Mexico. Mexico's output per worker fell from 42.3% to 32.8% of the US level. Output per worker relative to the US fell in 9 countries.
- **Closest to the line in 2019:** Panama (gap 0.475), the Bahamas (0.487), Uruguay (0.558) and Trinidad and Tobago (0.579).
- **Furthest from it:** Haiti (0.933), Nicaragua (0.882) and Honduras (0.869).

**Shares above the line.** The share of the population working in sectors at or above 50% of US output per worker is reported in the outputs but is not a useful summary at sector level. It jumps when a large sector crosses the line: in Panama it goes from 5% in 2000 to 33% in 2019, and in Costa Rica from 1% in 2019 to 27% in 2024. The average gap moves continuously with the step heights.

**Two caveats.** One price-level factor per country ignores differences in relative prices across sectors, which are large between tradables and services. Converting at 2020 price levels for all years also assumes that relative prices between each country and the US did not change. Venezuela and Cuba are excluded, as elsewhere (D-033).

## 5. What this does not show

- **Sector steps.** Everyone in a sector is placed at the sector average, so the ladders understate dispersion. A verdict of improvement at sector level is consistent with a deterioration for workers within a sector, and the reverse. This is the most important limitation (OQ-57).
- **Employment data.** ILO modelled employment fills the years between surveys. Grades indicate where the endpoints are anchored; the verdict counts above use grades A and B only.
- **Working-age population.** Ages 15+ includes people over 65. In the median well-anchored country their share of the 15+ population rose from 7.4% in 2000 to 10.5% in 2019, and in Uruguay, Barbados and Chile it was 15–19% by 2019. Ageing lowers the employment rate and therefore the employment-rate term. The zero block cannot yet separate people aged 65+: the ILO's employment estimates by age stop at a 25-and-over band (D-044, OQ-58).
- **Market output only.** Unpaid work is counted at zero.
- **Capabilities.** The definition refers to new and more complex activities, which sector ladders capture only indirectly.
- **No causal content.** Nothing here identifies what caused the changes. The verdicts describe outcomes, as the decompositions in WP05 and WP06 do. Which policies improve which parts of the distribution is a separate question that needs variation in policy (RG01, OQ-51).

## 6. Next steps

1. **Mexico with segment steps.** Use INEGI's informal-economy accounts for value added by sector and formal/informal status, the economic census for firm size, and ENOE for the employment split. Test P26. Check whether earnings ratios are a usable proxy for productivity ratios across segments (OQ-61).
2. **A 65+ block in the zero block**, from survey microdata where available (OQ-58).
3. **A check of the Baumol slope against independent sector deflators**, using the ETD for the countries it covers (OQ-59).

## References

Register IDs in brackets; status as recorded in `references/literature_register.csv`.

- Atkinson, A.B. (1987). On the measurement of poverty. *Econometrica* 55(4). [L140, from memory]
- Baumol, W.J. (1967). Macroeconomics of unbalanced growth: the anatomy of urban crisis. *American Economic Review* 57(3). [L144, from memory]
- Foster, J., Greer, J. & Thorbecke, E. (1984). A class of decomposable poverty measures. *Econometrica* 52(3). [L143, from memory]
- Foster, J.E. & Shorrocks, A.F. (1988). Poverty orderings. *Econometrica* 56(1). [L141, from memory]
- Infante, R. (ed.) (2011). *El desarrollo inclusivo en América Latina y el Caribe: ensayos sobre políticas de convergencia productiva para la igualdad*. CEPAL. [L138, partly verified]
- McMillan, M. & Rodrik, D. (2011). Globalization, structural change and productivity growth. NBER WP 17143. [L018]
- Ravallion, M. & Chen, S. (2003). Measuring pro-poor growth. *Economics Letters* 78(1). [L142, from memory]
- World Bank, Jobs Diagnostics tools (Job Structure tool; growth decompositions by sector and employment). [L139, verified]
