# Research log

One entry per work session, newest first.

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
