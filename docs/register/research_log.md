# Research log

One entry per work session, newest first.

---

## 2026-11-09 — Session 13: WP06 (LAC write-up); price-base correction

**Prompt (user):** finish the LAC productivity part: check the dashboard is ready, then write up the results; next, update Szirmai–Verspagen.

**Done**
- Dashboard readiness pass (see Session 12, last bullet), pushed.
- `07_lac_summary.py`: pooled decompositions for LAC, Latin America and the Caribbean (plus Caribbean without Guyana, and without Guyana and the Dominican Republic) at three price bases; country distributions; price-base agreement; pooled sector shares and relative productivity; value-added weights; three figures. Output in `empirics/output/lac_lp/summary/`.
- `papers/WP06_lac_structural_change/` (D-034): data and method changes from WP05, results, robustness, what the evidence does and does not show, links to P2, P3, P7.
- Correction D-035: dashboard default back to initial-year prices, with a robustness verdict for each country-period.

**What failed on the way:** writing the paper showed chained prices are not better-founded than fixed bases, as D-032 had claimed: chaining accumulates annual sampling noise in employment shares (37 of 109 grade A/B country-periods fall more than 0.1 pp outside the fixed-base bracket; Bolivia 2000–19 −0.24 chained vs +0.46/+0.38). Smoothing employment (3- or 5-year moving averages) moved as many cases out of the bracket as into it. Checking every number in the draft against generated output caught five errors (ranges quoted from one or two price bases instead of three, a sector attributed to telecoms alone, and an unsupported claim that the 2000–08 boom raised GDP growth); all fixed.

**Key results:** pooled LAC productivity growth fell from 1.7–1.9%/yr (1991–2000) to 0.30–0.35% (2008–19), almost all within sectors; the pooled structural term is positive at all three price bases after 2000 (0.14–0.17 pp, 2000–19) and sign-ambiguous in the 1990s; static gains with eroding relative productivity in absorbing sectors (70% of countries static > 0, dynamic < 0); 20 of 109 country-period structural terms change sign with the price base; Mexico's productivity fell despite robustly positive reallocation; Caribbean excluding Guyana and the Dominican Republic lost 1.4–1.5%/yr of productivity in 2008–19.

**Next:** the development-motors project (WP07): read Szirmai & Verspagen (2015) and the follow-up literature.

---

## 2026-11-09 — Session 12: LAC extension of the productivity panel; data files on GitHub

**Prompt (user):** (1) attach the repo and work in it as the author; (2) today's project is development motors (Szirmai–Verspagen and successors), but first: extend the Caribbean productivity analysis to the whole of LAC using ECLAC's country definitions, keeping a Caribbean section with the same content; (3) keep the source files on GitHub.

**Done**
- Repository attached; commits authored as Paul Wander. Added `CLAUDE.md` with authorship, voice and register conventions.
- World source files committed unmodified in `empirics/data/source/` with checksums (D-029): UN AMA files 2 and 6, ILO employment by activity (modelled and national sources) and the five ILO labour-market series. Same vintage as the Caribbean work: 82 UN series and all Caribbean ILO values identical (only Haiti's 2012 survey source code relabelled).
- Pipeline made scope-aware (`LP_SCOPE=lac|carib`, D-030). Rebuilding the Caribbean from the world files reproduces every published number.
- LAC panel: 33 countries, 1970–2024 value added; sector employment for 29 (not Antigua and Barbuda, Dominica, Grenada, Saint Kitts and Nevis). Grade-A country-periods in grid A: 15 of 29 for 2000–19, 21 for 2019–24. Modelled vs survey structural term, grid A: corr. 0.90, median gap 0.13 pp/yr, 92% same sign (114 pairs, 26 countries).
- New data rule (D-031): survey years covering under 80% of national employment are not used (urban-only surveys: Argentina, early Mexico, Uruguay before 2006, Bolivia 1991–92, Suriname).
- Chained price base added beside initial- and final-year prices (D-032); dashboard toggle with an explanatory note; chained is the default.
- Dashboard: region selector (LAC default, Caribbean), scope-aware loaders that are safe with several users, period-decomposition page with the price toggle and a robustness chart across price bases. Tested every page under both regions and all setting combinations (Streamlit AppTest), and in headless Chrome.
- Readiness pass on every LAC page in headless Chrome: ranking and annual-change charts now scale with the number of countries (they skipped every other label at 29), the employment scatter uses ISO3 labels when crowded (names on hover), and the labour-market line charts no longer stretch to 2040.
- D-029 to D-033; OQ-42 to OQ-45.

**What failed on the way:** the first LAC run gave Uruguay 3.5%/yr productivity growth for 2000–19 against 1.4% official: telecoms volume rose 7.5-fold, so valuing the period at 2000 prices over-weights it. This exposed a general weakness of fixed-base period decompositions (D-032). ILO's coverage notes did not flag Argentina's urban survey consistently, so coverage is tested from totals instead (D-031). Venezuela's 2020-price US$ levels are unusable as levels (D-033). Testing found two crashes, both fixed: a pre-existing one when an economy has fewer than two survey years on grid B (Haiti, in the original Caribbean dashboard too), and the country profile with survey employment for countries whose only survey is now excluded (Argentina). The dashboard's coverage map now shows excluded (non-national) surveys in their own colour.

**Key results (first look, not yet interpreted):** the sign of the structural-change term depends on the price base for 11 of 74 grade-A LAC country-periods, so a finding about structural change in a given country should be read only where the three price bases agree. Bolivia 2000–19 is the starkest case: positive at initial-year prices (+0.46 pp/yr), negative chained (−0.24), with large static and dynamic terms of opposite sign.

**Next:** the development-motors project (Szirmai–Verspagen replication) once PWT, ETD and the GGDC 10-sector files arrive.

---

## 2026-11-05 — Session 11: dashboard

**Prompt (user):** add a dashboard, runnable on the user's Streamlit account, using an ECLAC chapter draft as the reference for chart types and analysis; improvements allowed but kept separate and flagged.

**Done**
- Read the reference (L119): 25 charts; regional productivity (I.3–I.10), employment (I.2, I.11–I.13), IDPE (I.14), country panels A–J.
- User supplied five ILO modelled series; `06_extract_labour.py` extracts them (12 countries; capped at 2025).
- Built `empirics/dashboard/` (Streamlit + Plotly): 4 reference pages and 4 extended pages. The palette is validated with the dataviz validator; there is one fixed colour per sector.
- Tests:
  - every page loads in headless Chromium with no exceptions;
  - every page runs under all grid/series combinations and an empty aggregate (Streamlit AppTest), with one bug fixed (negative bar width for tiny sectors);
  - dashboard decompositions match WP05 outputs exactly (DOM, JAM, GUY, LCA checks), and annual identity error is under 1e-11.
- D-027; L119; OQ-40, OQ-41.

---

## 2026-11-05 — Session 10: decomposition design, validation, WP05 methodology

**Prompt (user):** keep the coverage information in a methodology section; (1) choose periods balancing rigour and coverage depending on how good the modelled estimates are; (2) run grid A and grid B separately; (3) handle constant-price non-additivity rigorously.

**Done**
- `03b_build_panel5.py` (grid B employment, incl. ILO six-group survey years); `decompose.py` (McMillan–Rodrik with static/dynamic split, initial- or final-year prices); `04_validate.py` (modelled vs survey employment between survey years); `05_decompose.py` (main + 3 robustness runs per grid, generated `results.md`).
- Validation: structural term with modelled employment tracks survey-based term (grid A corr. 0.91, median gap 0.14 pp/yr; grid B 0.85, 0.11). Failures: Suriname, Haiti (survey-type switches), Belize grid A (ISIC merges), Cuba 1990s.
- Decisions D-024 (initial-year prices), D-025 (two grids), D-026 (modelled employment, fixed periods, anchoring grades). Grade-A coverage: 23 country-periods / 9 countries (A), 28 / 11 (B). Survey-endpoint robustness for grade A: corr. 0.95.
- Wrote `papers/WP05_caribbean_structural_change/` with the full methodology section. Results generated but not interpreted.
- Register L118; OQ-36 closed; OQ-37–OQ-39 opened.

---

## 2026-11-05 — Session 9: Caribbean data loaded, coverage report

**Prompt (user):** four files attached (UN AMA constant 2020 and current US$; ILO EMP_2EMP and EMP_TEMP); produce a coverage report before discussing outputs.

**Done**
- Ran carib_lp on the real files; report in `empirics/output/carib_lp/coverage.md` (generated).
- Value added: all 16 countries, 7 sectors, 1970–2024. Constant-price sectors add up only in 2020 (chain-linking); current prices add up exactly.
- Modelled employment: 12 countries, 1991–2025; not ATG, DMA, GRD, KNA. Share of modelled years backed by a usable survey year ranges from 3% (Haiti) to 74% (Dominican Republic).
- Survey employment: usable 7-sector years from 0 (Dominica, Saint Kitts and Nevis) to 25 (Dominican Republic).
- Problems found and handled (D-023): negative derived mining in KNA (fixed via deflator); Jamaica 2023 broken (dropped); Barbados 2004–14 construction merged with mining (unused); missing ISIC sections reported, worst for Trinidad and Tobago, Cuba, Belize (OQ-33, OQ-34).
- Sanity check of 2019 productivity levels: plausible ordering (Bahamas and Barbados highest, Haiti lowest; Guyana mining jumps to ~US$364k per worker in 2023 with oil).

**Next:** discuss outputs with the user (decomposition design, periods, which employment series as baseline).

---

## 2026-11-05 — Session 8: Phase 2 starts — Caribbean productivity data

**Prompt (user):** is output and employment by sector available for Caribbean states, to build labour productivity and analyse it McMillan–Rodrik style? Start with the member states of ECLAC's Port of Spain office; record the work on GitHub.

**Done**
- Checked sources: the GGDC/UNU-WIDER ETD (L115) covers no Caribbean country, nor did the GGDC 10-sector database. Panel to be built from UN AMA value added (L116) and ILO employment (L117).
- Country list from caribbean.eclac.org/about: 16 members, 13 associate members (D-019).
- Found the UN AMA constant-price series is now at 2020 prices (latest upload January 2026), not 2015.
- Built `empirics/code/carib_lp/` (config, sector concordance, download, extract, panel + coverage report); smoke-tested end to end on synthetic files shaped like the UN and ILO downloads. No real data yet.
- Workspace cannot reach the UN/ILO sites; asked the user to attach the four files (D-022).
- Decisions D-019 to D-022; open questions OQ-27 to OQ-32; register L115–L117.

**Next:** load the files, review coverage, then the decomposition.

---

## 2026-11-03 — Session 7: visualizing the model's conclusions

**Prompt (user):** best way to visualize the main conclusions; then build the figures and an interactive version.

**Done**
- `model/visuals.py`: V1 landscape map (drift arrows, ridge, policy paths, before and after reform); V2 fiscal loop as a 45° fixed-point diagram (modern equilibrium τ ≈ 0.16, tipping point τ ≈ 0.51, trap at the ceiling where the budget would need 0.77); V3 attribution dot chart; V4 commodity ratchet with point of no return (year 8 of a 12-year boom).
- trapmodel 0.1.1: `attractors`, `classify`, `ridge` (code only; ridge matches the E1 grid).
- WP04 v0.2: summary section with the four figures; **correction D-017**: the trap does not strictly need the fiscal loop (at a fixed wedge near 0.50 the capability and learning loops alone give two steady states); the fiscal loop sustains it.
- Interactive explorer: `model/explorer/index.html` plus `explorer_data.py` (45 settings × 3 starts × 5 shocks); published as an artifact (D-018).

**Design notes:** the first V2 design (curves against the formal share) failed because, after the reform, every fixed wedge gives the same formal share; replaced by the 45° fixed-point diagram. V1 labels moved from a legend to direct labels.

---

## 2026-11-03 — Session 6: WP04 and trapmodel 0.1.0

**Prompt (user):** build a simple, illustrative model of LAC and other countries stuck in a middle-income trap; identify the main mechanisms; integrate into the project so it can be fine-tuned.

**Done**
- `model/`: trapmodel.py (three segments, managers, two goods, payroll-financed state, rents, ownership, K and A dynamics, six switches), five scenarios, run.py CLI, experiments.py (E1–E5), 20 tests (all pass), README, calibration register, CHANGELOG.
- `papers/WP04_trap_model/`: paper, figures, tables, auto-generated results.md.
- Framework §3b maps ideas to model objects; propositions P13–P24 tabulated; README updated.
- Register L113–L114 (from memory); D-015, D-016; OQ-22–OQ-26; OQ-01 partly closed.

**Development notes (what failed on the way):** with fixed spending levels the wedge was always at its ceiling; with spending as a GDP share the fiscal loop was inert because Cobb–Douglas demand ties informal income to formal income; indexing to total GDP exaggerated the commodity ratchet. Fixes in CHANGELOG.

**Key results:** two steady states (u ≈ 0.72–0.77 vs 0.03; GNI 2.6× apart); fiscal loop creates the trap; faster learning in tradables also escapes; K and A are complements; commodity ratchet conditional on proximity to threshold; Idea 5 and the remittance hypothesis fail in v0.1.

---

## 2026-11-03 — Session 5: relation to the middle-income trap literature

User asked how the project relates to the MIT literature. Read/verified Eichengreen–Park–Shin (2013), Im & Rosenblatt (2013), Bulman–Eden–Nguyen, Pritchett & Summers (2014), Doner & Schneider (seminar version), Agénor & Canuto (2015); Schneider (2013) via summary. Wrote `docs/literature/09_middle_income_trap.md`. Register L104–L112; D-014; OQ-20, OQ-21.

---

## 2026-11-02 — Session 4: novelty check

User asked what is publishable. Searched for prior art on the two core framework ideas. Found Fentanes & Levy (2024), Bobba et al. (2021), Franco & Quintero (2025) — L101–L103. Framework Ideas 1 and 3 annotated with prior art. Assessment recorded as D-013.

---

## 2026-11-02 — Session 3: WP02 (informality) and WP03 (foreign firms)

**Prompt (user):** (1) is informality a drag on growth or a symptom of poor dynamism — investigate fully; (2) foreign firms such as Coca-Cola: jobs, consumer gains, but rents leave and reduce the multiplier — discuss the growth impact without implying they should be excluded.

**Done**
- `papers/WP02_informality/WP02_informality_drag_or_symptom.md`: three-type typology (structural / policy-induced / evasive); symptom evidence (cheap formalization fails, falls with development, buffer, Chile); drag channels (formality wedge, unfair competition, staying small, narrow tax base, no learning); enforcement evidence; segment-choice threshold model and three loops; policy; P13–P16.
- `papers/WP03_foreign_firms/WP03_foreign_firms_rents_and_growth.md` + `rent_leakage.py`: Coca-Cola system (rent via concentrate pricing, local bottlers); five profit components; jobs (Costa Rica premium; Mexico retail displacement); consumer gains (Mexico supermarkets); supplier spillovers (Costa Rica, Lithuania) vs. negative horizontal (Venezuela); leakage table; FX asymmetry between export and domestic-market FDI; counterfactuals; P17–P20.
- Register L079–L100 (19 verified, 3 partly verified). Decisions D-011, D-012. Open questions OQ-15 to OQ-19.

**Key insights**
- Informality is "a symptom that becomes a cause". Chile's low informality with stagnant TFP is the strongest single piece of evidence that informality is not the root problem.
- Domestic-market FDI earns pesos but remits dollars — the precise mechanism behind the "rents leave" concern, linking WP03 to WP01's external constraint.
- Domestic owners who move savings offshore leak nearly as much domestic demand as foreign owners in the illustration; about half of 2025 FDI inflows were reinvested earnings.

---

## 2026-11-02 — Session 2: WP01, "Which firms are good for growth?"

**Prompt (user):** back to basics — how does a firm contribute to growth in the accounts (exports, imports on both sides of the ledger, wages, distribution, jobs that raise consumption without an equal rise in imports), rooted in theory, with sharp examples; output a working paper on GitHub.

**Done**
- Wrote `papers/WP01_which_firms/WP01_which_firms_are_good_for_growth.md`: three ledgers (production / income-and-demand / capability); corrects the "imports reduce GDP" reading of the expenditure identity; opportunity-cost measure of a job's contribution; GDP vs GNI (Ireland, Chile); open-economy multiplier and distribution (Bhaduri–Marglin); Thirlwall's law and net foreign exchange; five capability channels; seven-firm worked example; six common errors.
- `ledger_examples.py` generates Table 1 (illustrative parameters, maquila DVA calibrated to ~21%).
- Added L072–L078 to the register (6 verified, 1 partly verified). Decisions D-009, D-010. Open questions OQ-12 to OQ-14.

**Key insight for the framework:** the supermarket vs. corner-shop example shows Idea 5 (absorption constraint) at firm level — retail productivity rises ~3.6×, aggregate gain is only the net of displaced workers' alternative, and the external balance worsens.

---

## 2026-11-02 — Session 1: setup, background reading, framework v0.1

**Done**
- Created repository structure, README, research questions (`docs/research_questions.md`), registers.
- Background reading across eight strands; 71 sources entered in `references/literature_register.csv` (24 verified and 2 partly verified against sources this session; the remaining 45 flagged *from-memory* per D-007).
- Wrote strand notes `docs/literature/01–08` and synthesis `00_synthesis.md` with a 13-item LAC fact base and five tensions.
- Drafted `docs/theory/01_framework.md` (five ideas) and `02_propositions.md` (P1–P12).

**Key things learned / verified this session**
- IMF (2025, L041): LA5 TFP ~52% of US; TFP growth ≈ −0.7%/yr 2000–19; weakness within surviving firms; imposing other regions' industry mix barely changes LA5 TFP growth. This was the trigger for Idea 1 (segments vs. sectors).
- Diao, McMillan & Rodrik (L019): LAC growth from within-sector gains, reallocation weak/negative — consistent with Idea 1.
- Lagakos et al. (L048): experience-wage profiles ~2× steeper in rich countries — basis for Idea 3.
- Eslava, Haltiwanger & Pinzón (L034), Levy (L033), World Bank (L040): firm-structure and social-contract facts — basis for Idea 4 loops 1–2.
- Fujiwara & Matsuyama (L022) and Huneeus & Rogerson (L023): premature deindustrialization can arise from technology gaps / slow agricultural catch-up, not only trade.
- ILO–World Bank (L054): GenAI exposure 26–38% of LAC jobs; gains skew to formal workers — new-technology dimension of unbundling.

**Decisions:** D-001 to D-008.

**Open:** OQ-01 to OQ-11. Next priorities: OQ-06 (verify F9 from full IMF text), OQ-01 (formal model of the low equilibrium), OQ-07 (reading list), OQ-10 (verify from-memory entries).
