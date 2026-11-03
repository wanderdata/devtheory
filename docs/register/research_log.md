# Research log

One entry per work session, newest first.

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
