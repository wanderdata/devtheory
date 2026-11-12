# Defining and measuring productive development (v0.1, 2026-11-12)

This note sets out a working definition of productive development and the rules for measuring changes in it. The measurement is implemented in `empirics/code/lp/08_ladder.py` and `09_baumol.py`; results and discussion are in WP08. Decisions: D-042 (definition), D-043 (measurement choices).

## 1. The problem

Two definitions are in use in policy discussion in the region.

- **Productivity only.** Productive development is growth of labour productivity (output per employed worker). Its weakness: measured productivity can rise while output per person falls. When low-productivity workers lose their jobs, average productivity rises by composition. This happened in many countries in 2020.
- **Output per working-age person.** Productive development is growth of GDP per capita net of the demographic term, which is the same thing as growth of output per working-age person. In logs it is productivity growth plus employment-rate growth. Its weaknesses: (a) it is an outcome measure and says nothing about the productive structure, which is what the term has meant in ECLAC's work since Pinto; (b) it counts any rise in the employment rate as progress, including people entering very low-productivity work because household income fell.

Two facts from the regional data bear on the choice (WP08 §3):

- Productivity and the employment rate often move in opposite directions, at every horizon. The share of windows with opposite signs is 41–50% for windows of 1 to 20 years.
- The employment-rate term matters much less as the horizon lengthens. Its share of the variance of growth of output per working-age person falls from 27% for one-year windows to 8% for twenty-year windows.

So the two definitions disagree often in the short run and seldom in the long run, and the disagreement is mostly about the employment-rate margin.

## 2. Definition

**Productive development is a sustained improvement in the distribution of the working-age population across the productivity of the work they do, with people not in work counted at zero.** The improvement must come from the productive structure: better activities, more productive firms, and more people working in them. Changes due only to relative prices, the business cycle or demographics do not count.

Write $F_t$ for the distribution of the working-age population over productivity $y$, with the non-employed at $y = 0$. Three features of $F_t$ correspond to three concerns in the literature:

| Feature of $F_t$ | Concern it captures | Measure |
|---|---|---|
| Mean | Output per working-age person (the second definition above) | $\int y\,dF_t = Y/W$ |
| Upper part | Frontier activities and new, more complex ones; the main source of sustained productivity growth | Productivity and width of the top steps; diversification (not yet measured here) |
| Lower part and spread | Structural heterogeneity: the share of people in low-productivity work or none | Share and depth below a productivity line |

The definition settles two cases that the single-number definitions get wrong:

- **Composition effects.** If low-productivity workers lose their jobs, they move from a low step to zero. $F_t$ worsens at the bottom, so average productivity rising for this reason is not counted as development.
- **Distress employment.** A person moving from inactivity to near-zero-productivity work moves from zero to a slightly positive value. This is a small improvement, of about the size the definition should give it.

## 3. Measuring a change

Comparisons are between two dates at least five years apart and use constant-price volumes. Five tools are used, from the strictest to the least strict.

1. **First-order dominance.** $F_T$ lies on or below $F_0$ everywhere (every percentile of the working-age population is at least as productive). This is an improvement under any criterion that prefers more output.
2. **Second-order dominance.** The generalised Lorenz curve $GL(p) = \int_0^p Q(u)\,du$ is at least as high at every $p$. This is an improvement under any criterion that prefers more output and gives at least as much weight to gains at lower percentiles.
3. **Incidence curve.** $[Q_T(p) - Q_0(p)] / \mu_0$ per year, at each percentile $p$. Its average over percentiles equals the growth of the mean. It shows where gains and losses occurred.
4. **Decomposition of the mean.** Log growth of $Y/W$ splits exactly into within-sector productivity, structural change and the employment rate. Two terms are reported beside it: the demographic term ($W/N$) and the terms-of-trade gain.
5. **Threshold indices.** These are the Foster–Greer–Thorbecke family applied to productivity: the share of the working-age population below a line $z$, the average gap and the squared gap.

**Verdict.** "Improvement" means first-order dominance at both initial- and final-year prices. "Improvement, weighting the lower percentiles" means second-order dominance at both. "Deterioration" and its weighted form are defined the same way. "Ambiguous" means the ladders cross. "Depends on prices" means the two price bases give different results. This follows the project's practice of reporting a result only where reasonable treatments agree (D-035, D-040).

### Prices

- **Price windfalls.** Volume measures already exclude windfalls from export prices. A rise in the copper price does not raise mining's output per worker at constant prices. It does raise national income, so the terms-of-trade gain is reported separately: real gross domestic income over real GDP, with exports deflated by import prices.
- **Price bases.** Relative prices also affect the weights. A period valued at initial-year prices weights each sector by its prices in that year. Verdicts are therefore required to hold at final-year prices too.

## 4. Practical choices and their limits (D-043)

- **Working-age population.** The working-age population is everyone aged 15 and over. This matches the ILO employment and employment-ratio series, so the employed and the population refer to the same people. Workers aged 65+ are included in the sector steps, so excluding people aged 65+ from the population would leave the employed inconsistent with it. The zero block is split into the unemployed and people outside the labour force. People aged 65+ and not employed will be shown separately once ILO population and employment by age are added (OQ-58).
- **Steps.** With sector data, each sector is one step at its average output per worker. The ladder therefore understates dispersion: the spread within sectors is not observed. A dominance result at sector level is a statement about sector averages (OQ-57). Splitting sectors into formal and informal, or by firm size, adds steps. This is planned first for Mexico (INEGI's informal-economy accounts, economic census, ENOE).
- **Productivity line.** $z$ is output per employed worker at the start of the period, at the same prices, with $z/2$ as a second line. It is fixed within a period and not tied to the end-of-period mean, so it does not move with the outcome. A frontier-based line would allow comparisons across countries (OQ-60).
- **Unpaid work.** Unpaid care and household production are counted at zero, as in the national accounts. A rise in female participation therefore shows up as a gain in market output. That is correct for output, but it is not a gain in total production (OQ-58).
- **Weights.** The mean weights a gain anywhere equally. Second-order dominance gives more weight to the bottom without choosing how much. Any single welfare-weighted index requires a value judgement, which should be stated if one is used.
- **Capabilities.** The definition refers to new and more complex activities. Sector ladders capture these only when they change the step heights or widths. Measures of diversification and export complexity are a separate, leading indicator and are not implemented here.

## 5. Relation to the framework

In the notation of `01_framework.md`, the ladder with sector × segment steps ($s, m$) is the empirical counterpart of the framework's productivity distribution. The *T* segments are the low steps and the zero block is outside both segments. Propositions P1 and P2 concern movements between low and high steps within sectors. P3, which says no activity combines high labour absorption with high dynamism, implies that ladders will often cross. A dynamic activity raises a high step without widening it. An absorbing activity widens a low step without raising it. A "motor" in the sense of WP07 is an activity that raises and widens high steps while drawing people from the zero block and the low steps. P25–P27 (`02_propositions.md`) are the propositions specific to this note.
