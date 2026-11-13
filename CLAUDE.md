# Working conventions for this repository

Research project on productive development in Latin America and the Caribbean. Author: Paul Wander (Division of Production, Productivity and Management, UN-ECLAC). See `README.md` for the map.

## Authorship and voice

- Commits are authored as `Paul Wander <pjwander@gmail.com>`; set `git config user.name/user.email` in a fresh clone.
- Write as a careful development economist: precise, argued, sceptical of one's own results, plain English, no hype. State what the evidence shows, what it does not, and what would change the conclusion.
- Papers and app text must read as written by an economist, not generated: no dramatic phrasing, no sentences built for effect, no stock devices ("not X but Y" contrasts, rhetorical questions, triads, "crucially", "it's worth noting"). Keep technical detail (definitions, units, samples, caveats) even when it makes a sentence plainer.
- Papers are written as academic work for outside readers: outward-facing section titles (e.g. "Data", "Results", "Robustness"), not process titles ("gaps relative to the plan", "what failed"). Procedural material (deviations from a pre-analysis plan, choices made after seeing the data, implementation notes, further needs) goes in an annex at the end. The registers keep the full process record.

## Registers (mandatory)

- Every work session gets a dated entry in `docs/register/research_log.md` (newest first): prompt, what was done, key results, what failed.
- Every framing, scope, data or definitional choice gets a numbered entry in `docs/register/decision_log.md` (D-001, ...). Never delete; mark superseded.
- Unresolved issues go in `docs/register/open_questions.md` (OQ-01, ...).
- Every source read or cited gets a row in `references/literature_register.csv`, marked *verified* (checked against the source here) or *from-memory*. Paraphrase; note page or section.
- Propositions are numbered (P1, ...) and each says what evidence would support or reject it.

## Branches and deployment (D-036)

- Work on the `dev` branch. `main` is what the Streamlit apps deploy from; merge `dev` into `main` only when the user approves.
- Before pushing: `pytest`, and after any pipeline change `python empirics/code/<project>/run_all.py` then `python scripts/check_outputs.py`. GitHub Actions runs the same checks on every push.
- Changing a published number is a decision (log it), and the reference tests in `empirics/code/*/tests/` must be updated in the same commit.

## Code and data

- Each empirical project has its own folder in `empirics/code/` with `config.py`, numbered steps, `run_all.py` and `tests/`; generated reports go in `empirics/output/` and are never edited by hand.
- Country codes, names and ECLAC groupings come from `empirics/common/countries.py`; never keep a private copy.
- Apps live in `apps/<project>/` and only display precomputed outputs; shared theme and chart helpers are in `apps/common/theme.py`.
- Dependencies are pinned in `requirements.txt` (root) and in each app's own `requirements.txt`.
- Small shared world source files are committed unmodified in `empirics/data/source/` (D-029); large raw files go in the uncommitted `empirics/data/raw/`.
- The workspace cannot reach UN, ILO, ECLAC, World Bank or GGDC sites (D-022); the user downloads and attaches files. GitHub raw content and package registries are reachable.
- Corrections to earlier results are recorded as decisions, not silently edited (see D-017).
