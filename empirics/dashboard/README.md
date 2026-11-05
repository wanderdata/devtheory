# Caribbean labour productivity dashboard

Paul Wander, Division of Production, Productivity and Management, UN-ECLAC.

Streamlit app for the `carib_lp` project (WP05). It reads only files committed in this repository, so it runs on Streamlit Community Cloud with no setup.

## Deploy on Streamlit Community Cloud

1. Go to share.streamlit.io and sign in with the GitHub account that can see `wanderdata/devtheory`.
2. **Create app → Deploy a public app from GitHub**.
3. Repository: `wanderdata/devtheory`, branch `main`, main file path: `empirics/dashboard/app.py`.
4. Python version 3.11 or later. Dependencies are in `empirics/dashboard/requirements.txt`, which Streamlit picks up from the app's folder.
5. Deploy. The app redeploys automatically on every push to `main`.

Run locally: `pip install -r empirics/dashboard/requirements.txt && streamlit run empirics/dashboard/app.py`

## Structure

| Section | Page | Contents |
|---|---|---|
| Baseline analysis (following McMillan & Rodrik) | Regional productivity | Level over time, ranking, annual change, within/structural-change components by year |
| | Sectors and structural change | Productivity ladder (relative productivity × employment share), sector trends, sector contributions to the within and structural-change components |
| | Employment | Productivity vs employment-rate quadrants, employment rate, Shapley split into participation and unemployment, unemployment and participation rates |
| | Country profile | Panels A–I for one country |
| Extended analysis | Anchored period decompositions | WP05 main results: grades, static/dynamic, robustness |
| | Annual decomposition, additive prices | Annual decomposition at previous-year prices, survey-year markers, price-base comparison |
| | Reallocation and productivity gaps | McMillan–Rodrik scatter with weighted slope; dispersion index; hours vs output per hour |
| | Data quality and coverage | Survey timeline, validation, model vs survey shares, grades |

### Data notes

- **Sectors.** 7 sectors (grid A) or 5 (grid B): UN value added for the Caribbean exists only at 7.
- **Latest year.** Sector data end in 2024, when UN value added ends. Labour-market series run to 2025 (ILO; later projections dropped).
- **Productivity measure.** Per worker in constant 2020 US$ by default; sector data are per worker. Per hour (ILO, 2021 PPP$) is available for whole-economy charts.

## Files

- `app.py`: navigation.
- `lib.py`: data loading, decomposition, chart helpers, and the palette (validated, colour-blind safe, one fixed colour per sector).
- `views/`: one file per page.
- Data come from `empirics/data/processed/carib_lp/`, `empirics/data/interim/carib_lp/ilo_labour.csv` (from `06_extract_labour.py`) and `empirics/output/carib_lp/`.
