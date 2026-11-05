# WP05 — Structural Change and Labour Productivity in the Caribbean, 1991–2024

*Draft v0.1, 2026-11-05. Data and method; results are a first pass, not yet interpreted.*

**Code:** [`empirics/code/carib_lp/`](../../empirics/code/carib_lp/README.md) · **Generated outputs:** [coverage](../../empirics/output/carib_lp/coverage.md), [validation](../../empirics/output/carib_lp/validation/validation.md), [results](../../empirics/output/carib_lp/results.md) · **Decisions:** D-019 to D-026

## 1. Purpose

Measure how much of labour-productivity growth in Caribbean economies since 1991 came from productivity growth within sectors and how much from workers moving between sectors with different productivity levels (McMillan & Rodrik 2011; Diao, McMillan & Rodrik 2017). The standard dataset for this exercise, the GGDC/UNU-WIDER Economic Transformation Database, covers no Caribbean country (L115), so the panel is built here from UN national accounts and ILO employment data.

## 2. Methodology

### 2.1 Country scope

The 16 member countries served by the ECLAC subregional headquarters for the Caribbean in Port of Spain (caribbean.eclac.org/about, checked 2026-11-05): Antigua and Barbuda, Bahamas, Barbados, Belize, Cuba, Dominica, Dominican Republic, Grenada, Guyana, Haiti, Jamaica, Saint Kitts and Nevis, Saint Lucia, Saint Vincent and the Grenadines, Suriname, Trinidad and Tobago. ECLAC's 13 Caribbean associate members (non-independent territories) are excluded for now (D-019).

### 2.2 Sources

| Variable | Source | Vintage used |
|---|---|---|
| Value added by sector, constant 2020 US$ | UNSD National Accounts Main Aggregates (AMA), "GDP and its breakdown at constant 2020 prices in US Dollars" | Upload of January 2026; downloaded 2026-11-05 |
| Value added by sector, current US$ | UNSD AMA, "GDP and its breakdown at current prices in US Dollars" | Same |
| Employment by sector, modelled | ILOSTAT `EMP_2EMP_SEX_ECO_NB_A` (ILO modelled estimates, thousands) | File stamped 2026-11-05 |
| Employment by sector, national sources | ILOSTAT `EMP_TEMP_SEX_ECO_NB_A` (labour force surveys, censuses, other household surveys; thousands) | File stamped 2026-11-05 |

Note that the UN constant-price series are now at 2020 prices (not 2015). Raw world files are not committed; 16-country extracts are (`empirics/data/interim/carib_lp/`), with provenance in `sources.csv`.

### 2.3 Sector grids

Two grids are analysed separately and not mixed (D-025). A choice between them will be made later.

**Grid A, 7 sectors** (D-020). This follows the UN AMA's groupings, which use ISIC Rev.3: agriculture (AGR, ISIC A–B); mining and utilities (MIU, C+E); manufacturing (MAN, D); construction (CON, F); trade, restaurants and hotels (TRH, G–H); transport, storage and communication (TSC, I); and other services (OTH, J–P: finance, real estate, business services, government, education, health, personal services). Seven sectors is the finest grid on which UN value added exists for all 16 countries. ILO employment is mostly in ISIC Rev.4 and is mapped to this grid with two known approximations:
- ISIC4 J (information and communication) goes to TSC. Under ISIC3, publishing was in manufacturing and computing in business services.
- ISIC4 E (water, sewerage, waste) goes to MIU. Under ISIC3, sewage and refuse were in other services.

The ILO modelled series publishes some ISIC4 sections in pairs (DE, HJ, LMN, RSTU). Each pair falls within one grid-A sector.

**Grid B, 5 sectors.** AGR, MIU, MAN, CON and services (SER = TRH + TSC + OTH). It can use survey years that ILO publishes only as six broad groups (agriculture; mining and utilities; manufacturing; construction; market services; non-market services). That adds survey coverage for Jamaica (15 years), Cuba (14), Suriname (9), Bahamas (7) and Trinidad and Tobago (6). The cost is that it cannot see any reallocation within services, which is where most Caribbean employment is.

In both grids, workers not classified by activity are allocated to sectors in proportion to the classified ones.

### 2.4 Coverage

**Value added.** All 16 countries have all 7 sectors in every year from 1970 to 2024.

**Employment.** The ILO modelled estimates cover 12 countries from 1991 to 2025. They exclude Antigua and Barbuda, Dominica, Grenada and Saint Kitts and Nevis. For those four, usable survey data are 2 years for Antigua and Barbuda (2001, 2018), 5 for Grenada (2018–23) and none for Dominica or Saint Kitts and Nevis, so **they cannot be included** (OQ-28).

For the 12 modelled countries, the share of the modelled years 1991–2024 that are also usable survey years (grid A) is:

| Country | Usable survey years (grid A) | Share of modelled years backed by a survey | Model vs survey sector shares, mean (max) gap, pp | Modelled/survey total employment |
|---|---|---|---|---|
| Dominican Republic | 25 | 74% | 0.4 (1.5) | 1.01 |
| Bahamas | 21 | 62% | 0.7 (7.8) | 1.08 |
| Saint Lucia | 21 | 62% | 1.1 (8.0) | 0.93 |
| Belize | 15 | 44% | 2.0 (13.5) | 0.94 |
| Jamaica | 15 | 44% | 0.2 (1.2) | 1.10 |
| Barbados | 8 | 24% | 0.4 (4.7) | 1.09 |
| Guyana | 7 | 21% | 1.1 (5.1) | 1.01 |
| Cuba | 6 | 18% | 0.8 (3.6) | 1.01 |
| Trinidad and Tobago | 6 | 18% | 2.9 (11.4) | 1.20 |
| Suriname | 5 | 15% | 2.6 (7.7) | 1.15 |
| Saint Vincent and the Grenadines | 2 | 6% | 0.2 (1.1) | 1.11 |
| Haiti | 1 | 3% | 6.9 (22.2) | 0.95 |

The full, regenerable report is in [`coverage.md`](../../empirics/output/carib_lp/coverage.md).

### 2.5 Data problems and rules

The rules below are in D-023 and applied in code.

1. **Mining and utilities in constant prices.** The UN publishes C–E (mining, manufacturing, utilities) and D (manufacturing) but not mining and utilities on their own. A constant-price residual (C–E minus D) goes negative under chain-linking (Saint Kitts and Nevis, 1970–89). MIU is therefore built as the current-price residual deflated by the C–E deflator. This assumes mining and utilities share the C–E price index, which is the only option with these data.
2. **Broken survey years.** Survey country-years with more than 25% of workers unclassified are dropped. This removes Jamaica 2023, where 54% are unclassified and some sector values are implausible (109,000 workers in electricity).
3. **Incomplete survey years.** Survey years missing any grid sector are not used. Barbados 2004–14 is the main case: construction is merged with mining there.
4. **Merged ISIC sections.** These are reported, not corrected. Some national surveys merge ISIC sections that ILO cannot separate. When the merge crosses grid-A sectors, the 7-sector survey split is distorted even though all sectors are present:
   - Trinidad and Tobago 2019–24 has no L, M, N or Q, and section J holds about 51,000 workers. Business services probably sit in TSC, which is 96,000 in the survey against 34,000 in the modelled series in 2019 (OQ-33).
   - Cuba 2011–14 has no G (trade), O or P.
   - Belize 2015–25 has no I or J (OQ-34).
5. **Survey source.** One survey source is used per country-year, preferring the labour force survey, then other household surveys, then the census. Switches between source types inside a country remain a source of breaks (Suriname, Haiti).

### 2.6 Which employment series: validation of the ILO modelled estimates

The modelled series is complete and has harmonized totals. But between survey years it is ILO interpolation and extrapolation, which smooths employment shares and would bias the structural-change term toward zero. To measure how far it can be trusted, every country with at least two usable survey years was decomposed over non-overlapping pairs of survey years at least four years apart. Each pair was run twice with identical value added: once with survey employment, once with modelled employment ([`validation.md`](../../empirics/output/carib_lp/validation/validation.md)).

| | Grid A | Grid B |
|---|---|---|
| Pairs (countries) | 37 (11) | 51 (12) |
| Correlation of structural-change term, model vs survey | 0.91 | 0.85 |
| Median absolute gap in structural term (pp/yr) | 0.14 | 0.11 |
| Mean absolute gap (pp/yr) | 0.36 | 0.34 |
| Pairs within 0.5 pp/yr | 81% | 82% |
| Same sign (or both below 0.25 pp/yr) | 95% | 86% |
| Mean bias, model minus survey (pp/yr) | +0.16 | +0.13 |
| Std. dev. of structural term, survey / model | 1.53 / 1.25 | 1.36 / 1.07 |
| Correlation of within term | 0.94 | 0.94 |

**Findings**
- **Structural term between survey years.** The modelled series reproduces it well in most cases.
- **Failures.** These cluster in three situations:
  - countries whose surveys switch type (Suriname 2004–13: −3.40 survey vs −0.45 model; Haiti 2003–12 in grid B);
  - years where ISIC sections are merged across grid-A sectors (Belize 2014–18: −1.80 vs −0.59 in grid A, but −0.33 vs −0.32 in grid B);
  - Cuba in the 1990s.
- **Smoothing.** The modelled series compresses the dispersion of the structural term by about a fifth, as expected from interpolation.
- **Within term.** The within term (and so total growth) differs more for individual pairs. This comes from total employment levels, not composition: survey totals jump when samples are redesigned or reweighted, while ILO totals are benchmarked to population estimates.

**Choice (D-026)**
- **Employment series.** The ILO modelled series is the main employment series for both grids.
- **Interpretation.** It is trusted only near survey years, where it carries survey information.
- **Periods.** Endpoints therefore need to be anchored, and anchoring is made explicit through the grades in §2.7.

### 2.7 Periods and anchoring grades

Fixed benchmark periods: **1991–2000, 2000–2008, 2008–2019, 2019–2024**, plus the long period **2000–2019**.
- 1991 is the first ILO modelled year.
- 2008 and 2019 avoid the global financial crisis and COVID troughs as endpoints.
- 2024 is the last year with value added.

Fixed periods keep countries comparable. Country-specific periods built around each country's survey years would be more rigorous but would make cross-country comparison impossible. The anchoring grade gives most of the rigour without that cost.

**Anchoring grades.** An endpoint is *anchored* if a usable survey year for that grid lies within two years of it.

| Grade | Endpoints anchored | Use |
|---|---|---|
| A | Both | Interpreted |
| B | One | Reported, flagged |
| C | None | Pure ILO model; appendix only, not interpreted |

Grades by country and period (grid A / grid B where different):

| Country | 1991–2000 | 2000–2008 | 2008–2019 | 2019–2024 | 2000–2019 |
|---|---|---|---|---|---|
| Bahamas | A | A | A | A | A |
| Barbados | C | C | B | A | B |
| Belize | A | B | B | A | A |
| Cuba | C / B | B / A | B | C | C / B |
| Dominican Republic | B | A | A | A | A |
| Guyana | B | B | B | A | A |
| Haiti | C | C | C | C | C |
| Jamaica | C / A | B / A | A | A | B / A |
| Saint Lucia | B | A | A | A | A |
| Suriname | C / A | C / B | C | B | C / B |
| Trinidad and Tobago | C | C | B | A | B |
| Saint Vincent and the Grenadines | A | B | C | C | B |

Grade-A coverage: 23 country-periods in 9 countries (grid A) and 28 in 11 countries (grid B). Haiti never reaches grade B, so its results are the ILO model's, not data.

### 2.8 Price base and additivity

UN constant-price series are chain-linked, so the seven sectors add up to total value added only in the 2020 base year. The largest departure is 27% for Guyana, and 11–13% for Dominica, Jamaica and Suriname. Current-price series add up exactly. A single distant base year would also mis-weight sectors whose relative prices moved a lot (oil, gold, bauxite, sugar).

So each period is valued at the prices of its own initial year (D-024):

$$Y_{i,0} = VA^{cur}_{i,t_0}, \qquad Y_{i,T} = VA^{cur}_{i,t_0}\cdot\frac{VA^{2020}_{i,T}}{VA^{2020}_{i,t_0}}$$

- **Additivity.** Sectors add up exactly, and aggregate growth is a Laspeyres volume index.
- **Exchange rates.** All sectors are converted at the same exchange rate, so the rate cancels out of the decomposition shares.
- **Grid B.** Services value added is the sum of the three re-valued service sectors, so it is additive too.
- **Final-year prices.** Valuing at final-year prices is the main robustness check.

**Check against official growth.** Aggregate growth from this construction is within 0.4 pp/yr of official growth (chain-linked total value added per modelled worker) in 78% of country-periods, and within 0.5 pp/yr in 83%. The large exceptions are where relative prices moved sharply:
- Guyana 2000–08: 11.4 against 7.0
- Guyana 2019–24: 79.1 against 83.9
- Haiti 1991–2000: 5.1 against 2.4
- Trinidad and Tobago 2000–08: 6.0 against 4.9

The `official_growth_pp` column in each results table reports this check.

### 2.9 Decomposition

With $p_i = Y_i/L_i$, $s_i = L_i/L$ and $P=\sum_i Y_i/L$, following McMillan & Rodrik (2011):

$$P_T - P_0 = \underbrace{\sum_i s_{i,0}\,(p_{i,T}-p_{i,0})}_{\text{within}} + \underbrace{\sum_i p_{i,T}\,(s_{i,T}-s_{i,0})}_{\text{structural change}}$$

The structural term splits into a **static** part, $\sum_i p_{i,0}\Delta s_i$, and a **dynamic** part, $\sum_i \Delta p_i\,\Delta s_i$ (de Vries, Timmer & de Vries 2015). Both are always reported, because McMillan and Rodrik's end-year weighting counts productivity growth in a shrinking sector as negative structural change:
- In Guyana 2000–19, farm employment fell from 27% to 15% of workers while farm productivity rose from average to 2.6 times average. The structural term is −3.1 pp/yr, all of it dynamic; the static part is zero.
- In Guyana 2019–24, oil sends the dynamic term to +7.6 pp/yr. Mining and utilities rose from 6.0% to 6.7% of workers while their productivity went from 2.9 to 11.7 times average.

**Units.** Terms are divided by $P_0$ and by the number of years. Each is a contribution to average annual productivity growth in percentage points per year (linear), so within + structural = growth. The code asserts that the identity holds exactly.

### 2.10 Robustness

For each grid:
- **R1, survey employment.** For grade-A country-periods, endpoints are the nearest usable survey years. The structural term agrees with the main run: correlation 0.95 in both grids, median absolute gap 0.15 pp/yr (A) and 0.08 (B).
- **R2, final-year prices.** Correlation with the main structural term is 0.90 (A) and 0.92 (B), with a median absolute gap of 0.07 pp/yr. Guyana's long period is the outlier: −3.06 at initial-year prices against −0.26 at final-year prices.
- **R3, excluding mining and utilities.** The sector is dropped from both value added and employment. This matters for Guyana (2019–24 structural term falls from 7.75 to 0.04) and for oil and mineral exporters generally (OQ-30).

### 2.11 Known limitations

- **Missing countries.** Four small OECS states are not in the panel, for lack of employment data.
- **Haiti, and Saint Vincent and the Grenadines after 2001.** These rest on ILO modelling, not data.
- **Seven sectors is coarse.**
  - Tourism is split between TRH and TSC.
  - Finance, business services and government are one sector (OTH).
  - The ISIC4-to-ISIC3 mapping moves small employment shares between TSC, MIU and OTH (OQ-29).
- **Enclave sectors** dominate the structural term where present (Guyana oil; Trinidad and Tobago oil and gas; bauxite in Jamaica, Guyana and Suriname). Results are always shown without them as well.
- **Employment levels differ between sources.** Modelled totals are up to 20% above survey totals (Trinidad and Tobago, Suriname 15%). This changes productivity levels and the within term, much less the structural term.
- **Cuba.** Value added in US dollars depends on its official exchange rate. Productivity levels across sectors are hard to compare, and the 2011–14 survey lacks a trade sector (OQ-31).
- **Mining and utilities deflator.** The C–E deflator is applied to mining and utilities (rule 1).

## 3. Results (first pass)

Generated tables:
- [`results.md`](../../empirics/output/carib_lp/results.md), all grids and periods;
- per grid, CSVs in `empirics/output/carib_lp/grid_A/` and `grid_B/`: `main`, `robust_survey`, `robust_final_prices`, `robust_no_mining`, and `sectors_main` (sector detail for productivity/employment-share scatter plots).

Not yet interpreted; to be discussed together with the choice between grids.

## References

See `references/literature_register.csv`: L018 (McMillan & Rodrik 2011), L019 (Diao, McMillan & Rodrik 2017), L115 (Kruse et al. 2022, ETD), L116 (UN AMA), L117 (ILOSTAT), L118 (de Vries, Timmer & de Vries 2015).
