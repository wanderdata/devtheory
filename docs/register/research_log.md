# Research log

One entry per work session, newest first.

---

## 2026-11-12 — Session 18: defining productive development; ladder of the working-age population

**Prompt (user):** summarise and assess an internal email exchange on whether productive development should be defined by productivity alone or by output per working-age person; propose a definition; then integrate the discussion into the repository. Style instruction: papers and app text should be plain and technical, without dramatic phrasing.

**Done**
- Definition (D-042): productive development as a sustained improvement in the distribution of the working-age population over the productivity of their work, non-employed at zero. Concept note `docs/theory/03_defining_productive_development.md`; propositions P25–P27.
- Pipeline steps `08_ladder.py` (log decomposition of output per working-age person; horizon statistics; ladders; first- and second-order dominance at two price bases; incidence curves; threshold indices) and `09_baumol.py` (relative-price split by sector; cross-sector slope), both scopes, with `ladder.py` and tests on constructed cases plus reference results. Measurement choices in D-043. Existing outputs unchanged.
- Productivity app: pages *Output per working-age person* and *Ladder of the working-age population*; relative-price section on the reallocation page. Checked in a browser.
- WP08 draft. OQ-57 to OQ-62; literature L138–L144. CLAUDE.md: style rule for papers and app text.
- Requested from the user: ILOSTAT `POP_2POP_SEX_AGE_NB_A` and `EMP_2EMP_SEX_AGE_NB_A`.

**Key results:** employment-rate term's share of the variance of growth of output per working-age person falls from 27% (1-year windows) to 8% (20-year); opposite signs in 41–50% of windows at every horizon. 2000–19, grades A/B: 7 of 23 countries show an unambiguous improvement, 9 are ambiguous (including Brazil, whose mean rose); none in 2008–19. Baumol slope −0.48 (2000–19), interval [−0.62, −0.29].

**Later in the session:** the user supplied ILOSTAT total population, ILO employment by age and the WDI 65+ share. Employment by age has no 65+ band and population by age is no longer in the ILOSTAT bulk list, so the 65+ block is not possible from these sources (D-044). Total population now comes from the ILO (adds Cuba and 2024); WP08 numbers unchanged otherwise.

**Continued (user: "ok continue"):** WP08 next steps feasible with data in hand (D-045): PPP frontier line and average gap below 50% of US output per worker (frontier.csv; new section on the ladder page; WP08 §4.6); terms-of-trade term with the average deflator (little difference); Baumol slope between survey years with survey vs modelled employment (−0.30 vs −0.34, 2000–19). OQ-60 and OQ-62 closed. The user approved merging `dev` into `main` as needed.

**ENOE (WP09) preparation:** pre-analysis plan written before opening data (D-046); method details of Donovan, Lu & Schoellman read from the IZA conference version (quarterly flows, tenure-based job-to-job, matching rules, raking; no misclassification correction; Mexico 1995–2017 in their sample); ENOE file description read for keys and precoded variables (P3R_ANIO/P3R_MES give the start date with the current employer). Code in `empirics/code/enoe/` with tests on synthetic panels. Data route: release assets of `wanderdata/enoe_data` (README pushed so releases can be created). Corrected during the work: the first version of `chain` could join two people who share a key at different points of the rotation; rewritten to assign ids link by link, with a test.

**What failed / corrections:** at sector level the share of the population above a frontier line jumps when one large sector crosses it (Panama 5% → 33%), so the average gap is used as the summary. A year selector on the new section could be left with no valid end year; fixed before commit. Figures given in conversation before the pipeline existed used the sum of sector value added for the horizon statistics (25% and 7% of variance) and a 15+ population; the pipeline uses official total value added (27% and 8%). In conversation I said productive development should be measured "net of terms of trade"; volume measures already exclude price windfalls, so the terms-of-trade gain is reported beside the measure instead (concept note §3). The proposed 15–64 working-age definition was dropped (D-043). A "smallest gain across percentiles" statistic was replaced by the share of percentiles that gained, because the narrow top step dominated it. The first draft of the Baumol note stated the direction of measurement-error bias wrongly; corrected before commit. The new ladder page was renamed because the *Sectors* page already has a "productivity ladder" of employed workers.

---

## 2026-11-10 — Session 17: beyond sector shares; three papers to read and replicate

**Prompt (user):** after WP07, broad-sector tests look mistaken; how would one design tests of which jobs, firms, sectors and other levels let an economy grow? Then: choose three recent papers that best develop these ideas, to review, replicate and draw LAC implications from.

**Done**
- Diagnosis of WP07's limits: wrong unit (within-sector heterogeneity), shares are outcomes not causes, "motor" bundles distinct mechanisms. Proposed a six-study programme (external demand shocks; places; firms; jobs; production networks; segments); not yet written up as a plan.
- Selected three papers with criteria fixed in advance (D-041): Lane (2025, QJE), Diao, Ellis, McMillan & Rodrik (2025, WBER), Donovan, Lu & Schoellman (2023, QJE). Citations and abstracts checked on RePEc; Lane's data and design checked in the arXiv version; Donovan et al.'s replication package located (Harvard Dataverse). Note `papers/reading_group/RG01_three_papers.md` with design, replication route, LAC proposition (P-RG1–3) and reading questions per paper. Literature register L135–L137; OQ-54 to OQ-56.

**What failed / limits:** Harvard Dataverse is not reachable from the workspace, so neither replication package's contents could be inspected; whether Lane's package is public is unconfirmed. The papers have not yet been read in full: the note says so, and its magnitudes for Lane come from the arXiv introduction. The II PND sector list and three near-miss citations are from memory.

---

## 2026-11-09 — Session 16: WP07 estimation, dashboard and draft

**Prompt (user):** keep going as far as possible unless an essential piece is missing.

**Done**
- Hausman–Taylor implemented and validated (D-038); RE/FE/BE via `linearmodels`.
- Five- and ten-year panel for 185 countries, 1950–2020 (D-038).
- Replication of S&V in three samples; questions 1–4; specification curve (192 specifications, 4,032 estimates); 68 tests pass across the repository (including WP07 construction rules and reference results).
- Dashboard `apps/motors/` (eight pages), checked page by page in a browser; every factual sentence checked against the outputs.
- WP07 draft (`papers/WP07_development_motors/WP07_development_motors.md`).
- D-038 to D-040; OQ-48 and OQ-49 closed; OQ-51 to OQ-53 opened.

**Key results:** S&V's unconditional manufacturing effect does not replicate (main HT −0.047, p = 0.23, vs +0.045); their interactions replicate almost exactly without former planned economies (−0.240 vs −0.241; +0.038 vs +0.027) but reverse without commodity exporters, because the income-gap interaction rests on 13 Gulf observations. Since 1990 the manufacturing share predicts slower growth (robustly negative 1990–2005, leaning negative 2005–20). LAC is never robustly different from the rest. No sector share robustly predicts faster growth after 2005 except agriculture (room to reallocate); services, and finance/business/government/personal services, robustly negative. In the ETD, manufacturing's employment share (not output share) predicts growth; business and financial services are drags.

**After deployment:** the overview's headline chart rendered blank on Streamlit Cloud. Cause: legend-only traces added after the last visual check made Plotly type the y axis as numeric, hiding the sector rows. Fixed by declaring the axis categorical; a new test fails any chart without data points or with legend-only traces on an untyped categorical axis (verified to fail on the broken version). Lesson: re-run the visual check after every chart change.

**What failed on the way:** pyarrow string types in PWT and the latitude file; ratio splice producing shares above 100 and inconsistent UN rows (caught by a test); a module-name clash between the two apps' `lib.py` (caught by the test suite); the specification curve silently dropping all ten-year specifications (caught by the dashboard chart); seven errors in page and paper text found by checking every number against outputs (LAC significance with FE, Kaldor range, undervaluation sign, Gulf years, superseded coefficients, a p-value, and an inaccurate claim about the commodity super-cycle). All fixed.

---

## 2026-11-09 — Session 15: WP07 data and literature; pre-analysis plan

**Prompt (user):** update Szirmai & Verspagen ("Bart's paper"): find it, read it, check recent literature, replicate and improve, and present findings in a Streamlit dashboard on four questions (is manufacturing still a motor; was it ever in LAC; why only in some contexts; other candidate motors, especially services).

**Done**
- Source files committed with checksums and licences: PWT 11.0, ETD (2021 release), GGDC 10-Sector (2015 release), Barro–Lee v2.2 (15+, fetched from the dataset's GitHub repository).
- Read the published S&V paper in detail (specification, estimators, tables, thresholds, gaps); mapped the follow-up literature (manufacturing still special; services as motors; LAC); 15 register entries (L120–L134), most abstract-only and marked partly-verified.
- Pre-analysis plan (D-037): data mapping, replication criteria, tests and readings for each of the four questions, pre-specified moderators with predicted signs, specification curve, limits.
- Coverage checks: UN manufacturing shares for 185 countries in 1970 (220 later); GGDC 10-Sector before 1970 for 30 countries (14 back to the 1950s, six Latin American); PWT growth for 111 countries in 1960 and 158 in 1970.

**What failed:** the S&V working-paper PDF host is not reachable from the workspace; the published version on Verspagen's site was. Barro–Lee's current release (v3) has no 15+ file on GitHub; v2.2 has, and is the vintage S&V used.

**Open:** OQ-48 (temperate-climate instrument), OQ-49 (validate a Hausman–Taylor implementation), OQ-50 (tourism data).

---

## 2026-11-09 — Session 14: repository restructuring (on `dev`)

**Prompt (user):** organise GitHub and the visualisation by best practice before the motors project; work on a `dev` branch, move the dashboard, restructure first.

**Done (D-036)**
- `dev` branch created; `main` untouched until the user approves the merge.
- `empirics/code/carib_lp/` → `empirics/code/lp/`; `empirics/dashboard/` → `apps/productivity/`; links updated in READMEs, papers and the dev container (registers keep their historical wording).
- Shared modules `empirics/common/countries.py` and `apps/common/theme.py`; the pipeline config and the app library import from them instead of keeping their own lists and helpers.
- `run_all.py` (both scopes, about two minutes); pinned `requirements.txt` (root and app); `pytest.ini`; 54 tests (country definitions, decomposition identities in every output file, chained-vs-fixed equivalence on one-year periods, reference numbers, every app page in both regions); `scripts/check_outputs.py`; GitHub Actions workflow.
- `CITATION.cff`; licences of UN, ILO and PWT data checked and recorded in the source README.

**Verification:** after the moves, every output was rebuilt from the committed sources. All 77 data, table and figure files are byte-identical to the pre-restructuring versions; the 7 generated Markdown reports differ only in the line naming the code path.

**What failed on the way:** the first GitHub Actions run failed at test collection: plain `pytest` (used by CI) does not put the repository root on the import path, while `python -m pytest` (used for the local check) does, so the shared module could not be imported. Fixed with `pythonpath = .` in `pytest.ini`; the local check now reproduces CI exactly (fresh clone, clean virtual environment from `requirements.txt`, plain `pytest`). Second run passed. Runner image pinned to ubuntu-24.04; actions updated to checkout@v5 and setup-python@v6.

**Next:** user merges `dev` into `main` and changes the Streamlit app's main-file path to `apps/productivity/app.py`; then the motors project (WP07).

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
