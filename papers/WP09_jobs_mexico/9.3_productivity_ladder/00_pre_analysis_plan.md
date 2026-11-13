# Study 9.3 — A productivity ladder for Mexico with formal and informal steps

*Paul Wander. Pre-analysis plan v0.1, 2026-11-13. Written before any segmented ladder was computed (D-052).*

## 1. Question and propositions

WP08 places every person aged 15+ at the output per worker of their sector, with the non-employed at zero, and compares the resulting ladders over time by stochastic dominance. For Mexico, with one step per sector, every period since 2000 is *ambiguous*: the ladders cross. Sector averages hide the split between formal and informal work, which in Mexico covers more than half of employment. Formal and informal workers in the same sector differ greatly in productivity.

This study adds formal and informal steps within each sector. It asks two questions:
- **(a)** whether the WP08 verdicts change (P26, stated in WP08);
- **(b)** how much of the change in output per working-age person comes from reallocation between the formal and informal parts of each sector, which a sector-level decomposition counts as within-sector productivity change (OQ-46; P1–P2).

**P26 for Mexico.** Splitting sectors into formal and informal steps makes the verdicts worse.
- **Supported if,** in at least two of the four periods of §2, the segmented verdict is lower than the sector-only verdict in the order: improvement > improvement weighting the lower percentiles > ambiguous > deterioration weighting the lower percentiles > deterioration.
- **Rejected if** no verdict changes, or if changes go in the other direction.
- **Inconclusive** otherwise.

**P30.** Within-sector reallocation between formal and informal work is a material part of Mexico's within-sector productivity term.
- **Supported if,** for 2005–2019, the between-segment term within sectors has an absolute value of at least a quarter of the sector-level within term.
- **Rejected if** it is less than a tenth.

## 2. Data and periods

- **Employment and the working-age population:** ENOE, the average of the four quarters of 2005, 2008, 2019 and 2024. Persons aged 15+ are classified as not employed or employed in a sector × formality cell.
  - *Sectors:* INEGI's `rama_est2`, mapped to the seven national-accounts sectors of WP06 and WP08. Codes 5 and 6 map to TRH, 7 to TSC, 2 to MIU, and 8–11 to OTH. Employment with no sector specified is distributed across sectors in proportion to specified employment, within each formality status.
  - *Formality:* `emp_ppal`.
- **Value added:** UN National Accounts Main Aggregates, seven sectors, as in WP08. Each period is valued at its initial-year and final-year prices.
- **Periods:** 2005–2008, 2008–2019, 2019–2024 and 2005–2019. ENOE begins in 2005, which replaces WP08's 2000.

## 3. Splitting a sector's productivity between formal and informal workers

National accounts give value added *Y_s* by sector. ENOE gives employment *L_{s,f}* by sector and formality, and mean monthly labour income *e_{s,f}* among workers with positive income.

Output per worker in each cell is set to

  v_{s,f} = (Y_s / L_s) × (e_{s,f})^θ / Σ_f (L_{s,f}/L_s)(e_{s,f})^θ

This preserves each sector's value added exactly: Σ_f L_{s,f} v_{s,f} = Y_s. With θ = 1, productivity differs between formal and informal workers in a sector in the same proportion as their earnings.

- **Main specification:** θ = 1.
- **Sensitivity:** θ = 0.5, 1.5 and 2.

The earnings ratio probably *understates* the productivity gap. Formal firms have higher capital shares than informal units, so their value added per worker exceeds their wage bill per worker by more. θ > 1 shows how the verdicts depend on a wider gap. Calibrating the gap to INEGI's measurement of the informal economy, which reports value added by formal and informal status, is left for the next stage, when other data are brought in.

Unpaid family workers (`pos_ocu` = 4) are placed at their cell's value, not at zero, since they contribute to the cell's output.

## 4. Analyses

1. **Sector-only and segmented ladders** for each year and price base, with ENOE employment in both. The only difference between them is then the split.
2. **Verdicts** by first- and second-order dominance at both price bases, as in WP08 (functions in `empirics/code/lp/ladder.py`). The share of percentiles that gained and the incidence curve are reported with them.
3. **Decomposition of growth of output per working-age person** at the segment level:
   - within-segment;
   - between segments within sectors;
   - between sectors;
   - employment rate.

   This is compared with the sector-level decomposition (P30). The between-segment term within sectors is the static reallocation term computed on segments minus the one computed on sectors, so the two decompositions add up to the same total.
4. **Consistency check:** the sector-only ladder with ENOE employment against the WP08 ladder with ILO modelled employment.
5. **Robustness:**
   - θ = 0.5, 1.5, 2;
   - median instead of mean earnings;
   - steps by sector × formality × firm size (two classes), with the caveat that firm size is misreported (study 9.1).

## 5. What would change the conclusions

- **Implausible implied gap.** If the implied informal/formal productivity ratio in a sector is above 1, or below 0.1, the earnings proxy is not credible for that sector. Its split is then reported but not used, and the sector enters as one step.
- **Earnings non-response.** If it differs between formal and informal workers in a sector by more than 20 percentage points, the ratio is computed with medians and reported both ways.

## 6. Outputs

Code is in `empirics/code/enoe/ladder/`; tables go to `empirics/output/enoe/ladder/`; the paper is `01_paper.md`; the app page is "9.3 A productivity ladder for Mexico".
