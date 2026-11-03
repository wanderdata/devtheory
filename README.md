# Productive Development in Latin America and the Caribbean

A research project on how countries grow and develop, what economic structure that requires, whether some jobs and sectors are better than others, and why Latin America and the Caribbean (LAC) has grown so slowly for so long.

The project builds on the established economic literature (growth theory, structural change, dual economy, misallocation, complexity, good jobs) and proposes some new ideas to refine how we think about growth and development, with LAC as the central case.

**Phase 1 (current): theory.** Literature review, conceptual framework, and a set of testable propositions.
**Phase 1b (current): modelling.** A minimal, tunable model of the trap (`model/`, WP04).
**Phase 2 (later): empirics.** Testing the propositions with country, sector and firm data.

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
| `docs/theory/` | Conceptual framework, new ideas, and testable propositions |
| `papers/` | Working papers, each in its own folder with the code that generates its numbers. **WP01:** [Which Firms Are Good for Growth?](papers/WP01_which_firms/WP01_which_firms_are_good_for_growth.md) · **WP02:** [Informality: Drag or Symptom?](papers/WP02_informality/WP02_informality_drag_or_symptom.md) · **WP03:** [Foreign Firms, Rents and Growth](papers/WP03_foreign_firms/WP03_foreign_firms_rents_and_growth.md) · **WP04:** [A Segment Trap (model)](papers/WP04_trap_model/WP04_segment_trap_model.md) |
| `model/` | **trapmodel**: tunable model of the middle-income segment trap (scenarios, switches, tests, calibration register). See [model/README.md](model/README.md). Interactive explorer source in `model/explorer/` |
| `docs/register/research_log.md` | Dated log of every work session: what was done, read, decided |
| `docs/register/decision_log.md` | Numbered decisions with rationale (definitions, scope, framing choices) |
| `docs/register/open_questions.md` | Unresolved issues and things to check |
| `references/literature_register.csv` | Every source consulted: citation, strand, key claim, LAC relevance, status |
| `references/references.bib` | BibTeX for cited works |
| `empirics/` | Reserved for Phase 2 (data, code, output) |

## Conventions

- Every work session gets an entry in the research log.
- Every framing or definitional choice gets a numbered entry in the decision log (D-001, D-002, ...).
- Every source read or cited gets a row in the literature register. Claims from sources are paraphrased; page/section noted where possible. Status distinguishes *verified* (checked against source in this project) from *from-memory* (standard result, to be checked).
- Propositions are numbered (P1, P2, ...) and each states what evidence would support or reject it.
