# Productive Development in Latin America and the Caribbean

A research project on how countries grow and develop, what economic structure that requires, whether some jobs and sectors are better than others, and why Latin America and the Caribbean (LAC) has grown so slowly for so long.

The project builds on the established economic literature (growth theory, structural change, dual economy, misallocation, complexity, good jobs) and proposes some new ideas to refine how we think about growth and development, with LAC as the central case.

**Phase 1 (current): theory.** Literature review, conceptual framework, and a set of testable propositions.
**Phase 1b (current): modelling.** A minimal, tunable model of the trap (`model/`, WP04).
**Phase 2 (started 2026-11-05): empirics.** Testing the propositions with country, sector and firm data. First project: a sectoral labour-productivity panel for the Caribbean, extended on 2026-11-09 to all 33 LAC member States of ECLAC ([`empirics/code/lp/`](empirics/code/lp/README.md)), with a Streamlit dashboard that switches between the two ([`apps/productivity/`](apps/productivity/README.md)).

## Core research questions

1. **How do countries grow and develop?** What are the proximate and deep sources of sustained growth?
2. **What economic structure is needed?** Which types of jobs, sectors and firms carry growth, and does the sequence matter?
3. **Are some jobs better than others?** In what precise sense — productivity level, productivity growth, spillovers, learning, stability, tradability?
4. **Why does LAC grow so slowly?** What explains the region's low and stagnant productivity relative to its income level and endowments?

See [`docs/research_questions.md`](docs/research_questions.md) for the full, decomposed question tree.

## Repository map

| Path | Contents |
|---|---|
| `docs/research_questions.md` | Questions, sub-questions, and what would count as an answer |
| `docs/literature/` | Literature review, one note per strand |
| `docs/theory/` | Conceptual framework, new ideas, testable propositions, and the working definition of productive development (`03_defining_productive_development.md`) |
| `papers/` | Working papers, each in its own folder with the code that generates its numbers. **WP01:** [Which Firms Are Good for Growth?](papers/WP01_which_firms/WP01_which_firms_are_good_for_growth.md) · **WP02:** [Informality: Drag or Symptom?](papers/WP02_informality/WP02_informality_drag_or_symptom.md) · **WP03:** [Foreign Firms, Rents and Growth](papers/WP03_foreign_firms/WP03_foreign_firms_rents_and_growth.md) · **WP04:** [A Segment Trap (model)](papers/WP04_trap_model/WP04_segment_trap_model.md) · **WP05:** [Structural Change and Labour Productivity in the Caribbean](papers/WP05_caribbean_structural_change/WP05_caribbean_structural_change.md) · **WP06:** [Structural Change and Labour Productivity in Latin America and the Caribbean](papers/WP06_lac_structural_change/WP06_lac_structural_change.md) · **WP07:** [Development Motors: Is Manufacturing Still the Engine of Growth?](papers/WP07_development_motors/WP07_development_motors.md). **WP08:** [Defining and Measuring Productive Development](papers/WP08_productive_development/WP08_defining_productive_development.md). **WP09:** Job ladders in Mexico: [pre-analysis plan](papers/WP09_job_ladders_mexico/00_pre_analysis_plan.md), [first results](papers/WP09_job_ladders_mexico/01_first_results.md). `reading_group/`: reading and replication notes on outside papers, **RG01:** [Three papers beyond sector shares](papers/reading_group/RG01_three_papers.md) |
| `model/` | **trapmodel**: tunable model of the middle-income segment trap (scenarios, switches, tests, calibration register). See [model/README.md](model/README.md). Interactive explorer source in `model/explorer/` |
| `docs/register/research_log.md` | Dated log of every work session: what was done, read, decided |
| `docs/register/decision_log.md` | Numbered decisions with rationale (definitions, scope, framing choices) |
| `docs/register/open_questions.md` | Unresolved issues and things to check |
| `references/literature_register.csv` | Every source consulted: citation, strand, key claim, LAC relevance, status |
| `references/references.bib` | BibTeX for cited works |
| `empirics/` | Phase 2. `code/`: one folder per project, each with `config.py`, numbered steps, `run_all.py` and `tests/` (**lp:** sectoral labour productivity, Caribbean and LAC scopes; WP05, WP06). `common/`: shared country codes, names and ECLAC groupings. `data/source/`: downloaded files, unmodified, with checksums and licences; `interim/`, `processed/`: derived data, committed; `raw/`: not committed. `output/`: generated tables and figures |
| `apps/` | Streamlit dashboards, one folder per project, displaying precomputed outputs only. **productivity:** labour productivity and structural change, LAC and Caribbean ([README](apps/productivity/README.md)). **motors:** development motors, WP07 ([README](apps/motors/README.md)). `common/`: shared theme and chart helpers |
| `scripts/check_outputs.py`, `.github/workflows/` | Reproducibility check (rebuild everything, compare with committed outputs) and the GitHub Actions workflow that runs it with the tests on every push |

## Working with the repository

- **Branches.** Work happens on `dev`; `main` is what the apps deploy from and is updated by merging `dev` when a change is approved (D-036).
- **Reproduce.** `pip install -r requirements.txt`, then `python empirics/code/lp/run_all.py` rebuilds every labour-productivity output; `python scripts/check_outputs.py` confirms they match the committed versions; `pytest` runs all tests.
- **Cite.** See `CITATION.cff`, and the source licences in `empirics/data/source/README.md`.

## Conventions

- Every work session gets an entry in the research log.
- Every framing or definitional choice gets a numbered entry in the decision log (D-001, D-002, ...).
- Every source read or cited gets a row in the literature register. Claims from sources are paraphrased; page/section noted where possible. Status distinguishes *verified* (checked against source in this project) from *from-memory* (standard result, to be checked).
- Propositions are numbered (P1, P2, ...) and each states what evidence would support or reject it.
