# Caribbean labour productivity dashboard

Streamlit app for the `carib_lp` project (WP05). It reads only files committed in this repository, so it runs on Streamlit Community Cloud with no setup.

## Deploy on Streamlit Community Cloud

1. Go to share.streamlit.io and sign in with the GitHub account that can see `wanderdata/devtheory`.
2. **Create app → Deploy a public app from GitHub**.
3. Repository: `wanderdata/devtheory`, branch `main`, main file path: `empirics/dashboard/app.py`.
4. Python version 3.11 or later. Dependencies are in `empirics/dashboard/requirements.txt`, which Streamlit picks up from the app's folder.
5. Deploy. The app redeploys automatically on every push to `main`.

Run locally: `pip install -r empirics/dashboard/requirements.txt && streamlit run empirics/dashboard/app.py`

## Structure

| Section | Page | Reference (ECLAC chapter) |
|---|---|---|
| Reference analysis | Regional productivity | Charts I.3, I.4, I.5, I.6 |
| | Sectors and structural change | I.7, I.8, I.9, I.10 |
| | Employment | I.2, I.11, I.12, I.13 |
| | Country profile | Country panels B–J (I.15–I.25) |
| Extended analysis (not in the reference) | Anchored period decompositions | WP05 main results: grades, static/dynamic, robustness |
| | Annual decomposition, additive prices | I.6 at previous-year prices, survey-year markers, price-base comparison |
| | Reallocation and productivity gaps | McMillan–Rodrik scatter with weighted slope; dispersion index; hours vs output per hour |
| | Data quality and coverage | Survey timeline, validation, model vs survey shares, grades |

### Where the reference section departs from the reference, and why

- **Sectors.** 7 sectors (grid A) or 5 (grid B), not ECLAC's 9: UN value added for the Caribbean exists only at 7.
- **Latest year.** Sector data end in 2024, when UN value added ends. Labour-market series run to 2025 (ILO; later projections dropped).
- **Productivity measure.** Per worker in constant 2020 US$ by default; sector data are per worker. Per hour (ILO, 2021 PPP$) is available for whole-economy charts, as in the reference.
- **Panel B.** Productivity per hour and the employment rate are shown on one indexed axis (2005 = 100) instead of two axes.
- **Not reproduced.**
  - The productive development and employment index (IDPE: chart I.14 and country panel A), because its regression weights are not published.
  - Chart I.1 (GDP per capita by rolling decades), which needs population data that are not in the repository.

## Files

- `app.py`: navigation.
- `lib.py`: data loading, decomposition, chart helpers, and the palette (validated, colour-blind safe, one fixed colour per sector).
- `views/`: one file per page.
- Data come from `empirics/data/processed/carib_lp/`, `empirics/data/interim/carib_lp/ilo_labour.csv` (from `06_extract_labour.py`) and `empirics/output/carib_lp/`.
