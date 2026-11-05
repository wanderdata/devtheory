# Phase 2 data

- `raw/` — files as downloaded from the source. **Not committed** (see `.gitignore`); re-create with each project's download script.
- `interim/` — extracts of the raw files restricted to the countries in scope. Committed, so results can be rebuilt without the raw files.
- `processed/` — analysis-ready panels. Committed.

One subfolder per project (e.g. `carib_lp/`). Provenance of each interim file is in that folder's `sources.csv`.
