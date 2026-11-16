# A Productivity Ladder for Mexico with Formal and Informal Segments, 2005–2024

*Paul Wander. Working draft v0.2, 2026-11-16. Pre-analysis plan: [`00_pre_analysis_plan.md`](00_pre_analysis_plan.md). Generated tables: [`empirics/output/enoe/productivity_ladder/results.md`](../../../empirics/output/enoe/productivity_ladder/results.md). App: Jobs in Mexico, page 9.3.*

## Abstract

WP08 assesses productive development by the distribution of the population aged 15 and over across the output per worker of the activities in which they work, with the non-employed at zero, and compares distributions over time by stochastic dominance. For Mexico, with one productivity level per sector, the comparisons are ambiguous for every period since 2008. This paper splits each of seven sectors into formal and informal segments, using employment and labour income from the national labour-force survey (ENOE) for 2005, 2008, 2019 and 2024 to allocate national-accounts value added between them, with each sector's total preserved and the productivity gap set equal to the income gap raised to a power θ between 0.5 and 2. The dominance verdicts are unchanged in all four periods and all seven specifications. In a shift-share decomposition, the reallocation of employment from informal to formal segments within sectors contributes 0.07 percentage points a year to the growth of output per worker over 2005–2019 at θ = 1, against a sector-level within-sector term of −0.27; this contribution scales with θ and is a consequence of the assumed gap rather than an independent measurement.

## 1. Introduction

Sector averages of output per worker conceal the difference in productivity between formal and informal activity within sectors, which is large in Latin America (WP06). WP08 proposed assessing productive development by the distribution of the working-age population over the productivity of the work they do, with the non-employed at zero, and applied it to 29 countries with one productivity level per sector. It identified the resulting understatement of dispersion as its main limitation and stated, as proposition P26, that a finer split would make verdicts less favourable.

This paper tests P26 for Mexico, where informal employment accounts for more than half of the total, by splitting each sector into formal and informal segments. It also asks how much of what a sector-level decomposition records as productivity growth within sectors is reallocation between the formal and informal parts of a sector (proposition P30), which bears on the project's broader claim that Latin America's productivity problem lies within sectors rather than between them (propositions P1 and P2).

## 2. Data

Employment and population come from ENOE, as averages of the four quarters of 2005, 2008, 2019 and 2024. Persons aged 15 and over are classified as not employed or as employed, formally or informally (INEGI's labour-informality definition), in one of seven sectors aligned with the national accounts: agriculture; mining and utilities; manufacturing; construction; trade, restaurants and hotels; transport, storage and communications; and finance, business, government and personal services. Employment with no sector recorded, under 1%, is distributed in proportion to recorded employment.

Value added by sector comes from the UN National Accounts Main Aggregates, as in WP06 and WP08. Each period is valued at the prices of its initial year and, for the dominance comparisons, also at those of its final year. The periods are 2005–2008, 2008–2019, 2019–2024 and 2005–2019.

*Table 1. Informal share of employment by sector*

| Sector | 2005 | 2008 | 2019 | 2024 |
|---|---|---|---|---|
| Agriculture | 91.4% | 90.9% | 87.4% | 84.8% |
| Construction | 82.6% | 78.8% | 78.2% | 78.4% |
| Trade, restaurants and hotels | 64.5% | 63.2% | 63.0% | 62.0% |
| Transport, storage and communications | 57.4% | 55.0% | 51.7% | 46.0% |
| Manufacturing | 43.2% | 43.2% | 37.0% | 36.6% |
| Finance, business, government and personal services | 43.1% | 42.5% | 44.2% | 42.5% |
| Mining and utilities | 15.1% | 11.2% | 13.3% | 13.6% |

## 3. Method

Value added Y_s of sector s, with employment L_s, is allocated to segment f (formal or informal) so that output per worker in each segment is proportional to the segment's mean monthly labour income e_{s,f} raised to the power θ, and segment value added sums to the sector total:

v_{s,f} = (Y_s / L_s) · e_{s,f}^θ / Σ_f (L_{s,f}/L_s) e_{s,f}^θ.

With θ = 1, output per worker differs between segments in the same proportion as labour income. Mean informal income is between 34% and 70% of mean formal income in the same sector, depending on sector and year. The income ratio probably understates the productivity gap, because the capital share of value added is higher in formal production; values of θ up to 2 show the consequences of a wider gap. A variant replacing means with medians (an income-weighted average of the medians of establishment-size sub-cells, not the median of the sector × formality cell), and a further split by establishment size, are also reported. INEGI's own measurement of value added in the informal economy, which would allow θ to be calibrated, is not used here (Annex A).

The ladder places each person aged 15 and over at the output per worker of their segment, or at zero if not employed. As in WP08, the later ladder is compared with the earlier one by first- and second-order stochastic dominance at both price bases, and a verdict is recorded only if the comparison is the same at both. The growth of output per worker is decomposed into within and between terms on segments and on sectors, at initial-year prices (McMillan and Rodrik 2011); the difference between the two between terms is the contribution of reallocation between segments within sectors.

## 4. Results

### 4.1 Dominance verdicts

*Table 2. Dominance verdicts, initial- and final-year prices*

| Period | One level per sector | Formal and informal segments (θ = 1) |
|---|---|---|
| 2005–2008 | improvement, weighting the lower percentiles | improvement, weighting the lower percentiles |
| 2008–2019 | ambiguous | ambiguous |
| 2019–2024 | ambiguous | ambiguous |
| 2005–2019 | ambiguous | ambiguous |

No verdict changes when sectors are split, for any of θ = 0.5, 1, 1.5 or 2, for medians or for the further split by establishment size. With ENOE employment, the sector-level verdicts agree with those of WP08, which uses ILO modelled employment, for 2008–2019 and 2019–2024.

The verdicts are ambiguous because sectors at different levels of the ladder moved in opposite directions. Between 2008 and 2019, output per worker rose by 10% in agriculture, near the bottom of the ladder, and by 11% in transport and communications, while it fell by 15% in construction, 10% in manufacturing, 6% in trade, restaurants and hotels and 25% in mining and utilities. Between 2019 and 2024 it rose by 5% in agriculture and fell in four of the other six sectors. Splitting a sector moves its formal workers up and its informal workers down by similar proportions at both dates, so the crossings between sectors remain.

The share of the population whose position improved, at initial-year prices, does change with the split. It rises from 61.8% to 66.7% in 2008–2019 and from 60.8% to 64.6% in 2019–2024, and falls from 79.1% to 71.3% in 2005–2008; at final-year prices the split raises it in 2005–2008 (from 69.5% to 71.1%).

### 4.2 Decomposition

*Table 3. Contributions to the growth of output per worker (percentage points a year; θ = 1; initial-year prices)*

| Period | Growth | Within segments | Between segments within sectors | Between sectors | Within sectors (one level per sector) |
|---|---|---|---|---|---|
| 2005–2008 | 0.60 | −0.04 | 0.27 | 0.38 | 0.23 |
| 2008–2019 | −0.46 | −0.46 | 0.03 | −0.03 | −0.43 |
| 2019–2024 | −0.68 | −1.04 | 0.15 | 0.21 | −0.89 |
| 2005–2019 | −0.21 | −0.34 | 0.07 | 0.06 | −0.27 |

At θ = 1, the reallocation of employment from informal to formal segments within sectors makes a positive contribution in every period; with the further split by establishment size it is slightly negative in 2008–2019 (−0.015). The term also includes the dynamic component of reallocation. Over 2005–2019 it amounts to 0.071 points a year, 26% of the absolute value of the sector-level within-sector term. In 2005–2008 the sector-level within-sector gain of 0.23 points a year is more than accounted for by this reallocation, and output per worker within the formal and informal segments did not grow. After 2008 the reallocation term is small, and productivity within segments falls somewhat faster than productivity within sectors.

The reallocation term depends directly on the assumed gap. Over 2005–2019 it is 0.036 points a year at θ = 0.5, 0.107 at θ = 1.5 and 0.142 at θ = 2; with medians it is 0.057, and with the further split by establishment size 0.027. Because every shift towards formal employment raises measured output per worker whenever θ > 0, the term measures what reallocation would contribute if productivity differed as assumed, not an independently observed change.

### 4.3 Propositions

P26, that a finer split makes verdicts less favourable, is rejected for Mexico: no verdict changes. P30 required the reallocation term over 2005–2019 to reach at least a quarter of the sector-level within-sector term; at 26% it meets the threshold in the main specification but not at θ = 0.5 (13%), with medians (21%) or with the size split (10%), and is therefore supported narrowly and not robustly.

## 5. Limitations

The allocation assumes that productivity differences within sectors follow income differences. The verdicts do not depend on this over the range of θ examined, but the size of the reallocation term does, roughly in proportion to θ.

Formal and informal segments are themselves heterogeneous; the informal segment of trade includes both street vending and established small shops. A finer split, by position in employment or establishment size, would come closer to the distribution over workers. The split by establishment size changes nothing here, but establishment size is reported with substantial error in ENOE (study 9.1).

## 6. Conclusions

Splitting Mexican sectors into formal and informal segments does not change the dominance verdicts of WP08: the comparisons that are ambiguous with one level per sector remain ambiguous with two. The split changes the interpretation of the decomposition. Part of what sector data record as productivity growth within sectors is the movement of workers from informal to formal employment, all of it in 2005–2008 and about a quarter over 2005–2019, on the assumption that productivity differs as income does. On the same assumption, output per worker within the formal and informal segments has fallen since 2008, slightly faster than the sector figures indicate. A calibration of the gap with INEGI's informal-economy accounts would replace the assumption with a measurement.

## Annex A. Implementation notes and further work

The choices set out in the pre-analysis plan were applied without change: annual figures are four-quarter averages, unspecified sectors are distributed in proportion, and unpaid family workers are placed at their segment's value. The plan asked for a decomposition of output per working-age person with an employment-rate term; the paper reports output per worker, and the employment-rate term is in the output files (column `emprate_log_pp`). Neither safeguard rule of the plan was triggered: every informal-to-formal income ratio lies between 0.34 and 0.70, and every difference between formal and informal workers in the share reporting income is below 17 points, against a threshold of 20. The code is in `empirics/code/enoe/productivity_ladder/` rather than `ladder/` as written in the plan, to avoid confusion with study 9.1.

Further work could calibrate θ with INEGI's measurement of the informal economy, value added by sector and formal or informal status, whose method is documented in section 4.4 of INEGI's national-accounts methodology (open question OQ-68); split segments further by position in employment; and compute the decomposition annually and chained, as in WP06.

## References

McMillan, M. and Rodrik, D. (2011). Globalization, structural change and productivity growth. NBER Working Paper 17143. [L018]

Project papers WP06 and WP08 and study 9.1 of this programme; data sources as in WP08.
