# Working conventions for this repository

Research project on productive development in Latin America and the Caribbean. Author: Paul Wander (Division of Production, Productivity and Management, UN-ECLAC). See `README.md` for the map.

## Authorship and voice

- Commits are authored as `Paul Wander <pjwander@gmail.com>`; set `git config user.name/user.email` in a fresh clone.
- Write as a careful development economist: precise, argued, sceptical of one's own results, plain English, no hype. State what the evidence shows, what it does not, and what would change the conclusion.

## Registers (mandatory)

- Every work session gets a dated entry in `docs/register/research_log.md` (newest first): prompt, what was done, key results, what failed.
- Every framing, scope, data or definitional choice gets a numbered entry in `docs/register/decision_log.md` (D-001, ...). Never delete; mark superseded.
- Unresolved issues go in `docs/register/open_questions.md` (OQ-01, ...).
- Every source read or cited gets a row in `references/literature_register.csv`, marked *verified* (checked against the source here) or *from-memory*. Paraphrase; note page or section.
- Propositions are numbered (P1, ...) and each says what evidence would support or reject it.

## Code and data

- Each empirical project has its own folder in `empirics/code/`; generated reports go in `empirics/output/` and are never edited by hand.
- Small shared world source files are committed unmodified in `empirics/data/source/` (D-029); large raw files go in the uncommitted `empirics/data/raw/`.
- The workspace cannot reach UN, ILO, ECLAC, World Bank or GGDC sites (D-022); the user downloads and attaches files. GitHub raw content and package registries are reachable.
- Corrections to earlier results are recorded as decisions, not silently edited (see D-017).
