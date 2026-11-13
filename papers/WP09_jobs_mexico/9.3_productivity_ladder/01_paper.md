# A Productivity Ladder for Mexico with Formal and Informal Steps, 2005–2024

*Paul Wander. Working draft v0.1, 2026-11-13. Pre-analysis plan: [`00_pre_analysis_plan.md`](00_pre_analysis_plan.md). Generated tables: [`empirics/output/enoe/productivity_ladder/results.md`](../../../empirics/output/enoe/productivity_ladder/results.md). App: Jobs in Mexico, page 9.3.*

## Abstract

WP08 judges productive development by the distribution of the working-age population over the productivity of the work they do. For Mexico, with one productivity level per sector, that distribution shows no unambiguous improvement or deterioration over any period since 2000.

We split each sector into formal and informal workers. National-accounts value added is allocated between the two in proportion to their labour incomes in the national labour-force survey, so that each sector's total is preserved.

**Verdicts.** Splitting the steps does not change any verdict, in four periods and under every specification tried, including within-sector gaps twice as wide as the income gap.

**Reallocation.** The split reveals reallocation that sector data cannot show. Between 2005 and 2019, the movement of workers from informal to formal work within sectors added 0.07 percentage points a year to output per worker. Productivity within each formal or informal segment fell faster than the sector figures suggest: −0.34 against −0.27 points a year. In 2005–2008, all of the within-sector gain measured on sectors came from formalisation.

## 1. Introduction

Sector averages hide the distinction between formal and informal work that is central to productivity in Latin America (WP06). WP08 proposed judging productive development by the whole distribution of the working-age population across productivity levels, with the non-employed at zero. It applied this to 29 countries with one step per sector, and flagged the resulting understatement of dispersion as its main limitation (P26).

This paper removes part of that limitation for Mexico, where informal work accounts for more than half of employment. It addresses two questions:
- whether the verdicts change when sectors are split into formal and informal steps;
- how much of what a sector-level decomposition calls within-sector productivity growth is in fact reallocation between the formal and informal parts of a sector.

The second is a direct test of the project's propositions P1 and P2: that the region's productivity problem lies in segments within sectors, not between sectors.

## 2. Data

**Employment and population.** From ENOE, averaging the four quarters of 2005, 2008, 2019 and 2024:
- persons aged 15 and over are classified as not employed, or employed in one of seven national-accounts sectors as formal or informal workers;
- employment with no sector specified (under 1%) is distributed in proportion to specified employment.

**Value added.** UN National Accounts Main Aggregates, as in WP06 and WP08. Each period is valued at its initial-year prices and, for the verdicts, also at its final-year prices.

**Periods.** 2005–2008, 2008–2019, 2019–2024 and 2005–2019. ENOE starts in 2005.

**Informal shares.** The informal share of employment differs widely across sectors and changed slowly:

| Sector | 2005 | 2024 |
|---|---|---|
| Agriculture | 91% | 85% |
| Construction | 83% | 78% |
| Trade, restaurants and hotels | 65% | 62% |
| Transport, storage and communications | 57% | 46% |
| Manufacturing | 43% | 37% |
| Finance, business, government and personal services | 43% | 43% |
| Mining and utilities | 15% | 14% |

## 3. Method

**Allocation within sectors.** Value added Y_s of sector s is allocated between formal and informal workers so that output per worker in each segment is proportional to its mean monthly labour income raised to a power θ. Totals are preserved:

v_{s,f} = (Y_s / L_s) · e_{s,f}^θ / Σ_f (L_{s,f}/L_s) e_{s,f}^θ

**The size of the gap.** With θ = 1, productivity differs within a sector as labour income does. Informal workers earn 34–70% of what formal workers in the same sector earn, depending on sector and year.

The income ratio probably understates the productivity gap, because formal firms have higher capital shares than informal units. Values of θ up to 2 show the effect of a wider gap. The aggregate national-accounts measure of the informal economy published by INEGI, which would calibrate θ, is not used here (Annex A).

**Ladders and verdicts.** These follow WP08. The ladder places each person aged 15+ at the output per worker of their segment, or at zero if not employed. The later ladder is compared with the earlier one by first- and second-order stochastic dominance at both price bases.

**Decomposition.** The growth of output per worker is decomposed on segments and on sectors. The difference between the two "between" terms is reallocation between segments within sectors.

## 4. Results

### 4.1 Verdicts

| Period | One step per sector | Formal and informal steps (θ = 1) |
|---|---|---|
| 2005–2008 | improvement, weighting the lower percentiles | improvement, weighting the lower percentiles |
| 2008–2019 | ambiguous | ambiguous |
| 2019–2024 | ambiguous | ambiguous |
| 2005–2019 | ambiguous | ambiguous |

No verdict changes, under any specification: θ = 0.5, 1, 1.5 or 2, medians instead of means, or a further split by establishment size. P26 is rejected for Mexico.

The sector-only verdicts with ENOE employment agree with WP08's verdicts, which use ILO modelled employment, for 2008–2019 and 2019–2024.

**Why the split does not matter here.** The ladders cross because sectors at different heights moved in opposite directions.
- **2008–2019:** output per worker rose in agriculture (+10%), near the bottom of the ladder, and in transport and communications (+11%). It fell in construction (−15%), manufacturing (−10%), trade, restaurants and hotels (−6%) and mining and utilities (−25%).
- **2019–2024:** agriculture again rose (+5%) while most other sectors fell.

Splitting a sector moves its formal workers up and its informal workers down by similar proportions at both dates. The crossings between sectors therefore remain.

**Share of percentiles that gained.** This summary does change. With formal and informal steps, the share of the population whose position improved rises from 62% to 67% in 2008–2019 and from 61% to 65% in 2019–2024, but falls from 79% to 71% in 2005–2008.

### 4.2 Reallocation within sectors

Contributions to the growth of output per worker are in percentage points a year (θ = 1, initial-year prices):

| Period | Growth | Within segments | Between segments within sectors | Between sectors | Within sectors (one step per sector) |
|---|---|---|---|---|---|
| 2005–2008 | +0.60 | −0.04 | +0.27 | +0.38 | +0.23 |
| 2008–2019 | −0.46 | −0.46 | +0.03 | −0.03 | −0.43 |
| 2019–2024 | −0.68 | −1.04 | +0.15 | +0.21 | −0.89 |
| 2005–2019 | −0.21 | −0.34 | +0.07 | +0.06 | −0.27 |

**Formalisation raised output per worker in every period.** Over 2005–2019 it contributed +0.07 points a year, a quarter of the size of the sector-level within term. That meets the threshold set for P30, narrowly, in the main specification.

**Sensitivity.** The result depends on the width of the gap:
- **θ = 0.5:** +0.04 points a year;
- **θ = 2:** +0.14;
- **medians:** +0.06;
- **adding establishment size:** +0.03.

P30 is therefore supported in the main specification but not robustly.

**Productivity within segments fell faster than sector figures show.** In 2005–2008 the sector-level within-sector gain of 0.23 points a year was entirely formalisation; productivity within formal and within informal work did not grow. After 2008 the reallocation term is small, and within-segment productivity falls slightly faster than within-sector productivity.

## 5. Robustness and limits

- **The income proxy.** The allocation assumes that productivity differences within a sector follow income differences. With θ from 0.5 to 2 the verdicts are unchanged; the size of the reallocation term scales roughly with θ.
- **Two segments are still averages.** Formal and informal work are themselves heterogeneous: the informal segment of trade includes both street vendors and small shops. More steps (establishment size, position in employment) would be needed to approach the distribution over workers. Establishment size was tried and changes nothing, but it is poorly reported in ENOE (study 9.1).
- **Value added by segment.** The allocation does not use INEGI's own estimate of value added in the informal economy, which would anchor the gap. That is the natural next step.

## 6. Conclusions

For Mexico, splitting sectors into formal and informal steps does not change WP08's verdicts. What the ladder cannot settle at sector level, it cannot settle with two steps per sector either: Mexico's productive development since 2008 has been ambiguous.

The split does change the reading of the decomposition. Part of what sector data record as productivity growth within sectors is the movement of workers from informal to formal work: all of it in 2005–2008, about a fifth over 2005–2019. Productivity within the formal and informal segments has been falling since 2008, a little faster than the sector figures indicate.

## Annex A. Notes on implementation and further work

**A.1 Choices.** All were set out in the pre-analysis plan:
- **Annual figures.** Four-quarter averages for ENOE.
- **Unspecified sector.** Employment distributed in proportion.
- **Unpaid family workers.** Placed at their segment's value.
- **Safeguard rules (§5 of the plan).** Neither was triggered:
  - every informal/formal income ratio lies between 0.34 and 0.70;
  - every difference in income reporting between formal and informal workers in a sector is below 20 points.
- **Folder name.** The code is in `empirics/code/enoe/productivity_ladder/`, not `ladder/` as written in the plan, to avoid confusion with study 9.1's `ladders/`.

**A.2 Further work.**
- **Calibrate the within-sector gap.** Use INEGI's measurement of the informal economy (value added by sector and formal or informal status), which would replace the income proxy.
- **Extend the steps.** Split further by position in employment (employee, own-account, employer).
- **Annual series.** Compute the decomposition annually and chained, as in WP06.

## References

Project papers WP06, WP08 and study 9.1; data sources as in WP08.
