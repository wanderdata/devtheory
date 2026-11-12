# Labour productivity and structural change dashboard: Latin America and the Caribbean

Paul Wander, Division of Production, Productivity and Management, UN-ECLAC.

Streamlit app for the sectoral labour-productivity project (WP05). It reads only files committed in this repository, so it runs on Streamlit Community Cloud with no setup.

**Region.** A selector at the top of the sidebar switches every page between **Latin America and the Caribbean** (the 33 ECLAC member States in the region; default) and the **Caribbean** (the 16 member States served by ECLAC's Port of Spain office, the broad definition used since D-019). The Caribbean view shows the same pages and analysis as the earlier Caribbean-only dashboard (D-030, D-033). The choice is kept per session.

## Deploy on Streamlit Community Cloud

1. Go to share.streamlit.io and sign in with the GitHub account that can see `wanderdata/devtheory`.
2. **Create app → Deploy a public app from GitHub**.
3. Repository: `wanderdata/devtheory`, branch `main`, main file path: `apps/productivity/app.py`.
4. Python version 3.11 or later. Dependencies are in `apps/productivity/requirements.txt`, which Streamlit picks up from the app's folder.
5. Deploy. The app redeploys automatically on every push to `main`.

Run locally: `pip install -r apps/productivity/requirements.txt && streamlit run apps/productivity/app.py`

## Structure

| Section | Page | Contents |
|---|---|---|
| Baseline analysis (following McMillan & Rodrik) | Regional productivity | Level over time, ranking, annual change, within/structural-change components by year |
| | Sectors and structural change | Productivity ladder (relative productivity × employment share), sector trends, sector contributions to the within and structural-change components |
| | Employment | Productivity vs employment-rate quadrants, employment rate, Shapley split into participation and unemployment, unemployment and participation rates |
| | Country profile | Panels A–I for one country |
| Extended analysis | Anchored period decompositions | WP05 main results: grades, static/dynamic, robustness |
| | Annual decomposition, additive prices | Annual decomposition at previous-year prices, survey-year markers, price-base comparison |
| | Reallocation and productivity gaps | McMillan–Rodrik scatter with weighted slope; dispersion index; hours vs output per hour; relative prices and measured productivity by sector (Baumol slope) |
| | Output per working-age person | Growth of output per person aged 15+ split into within-sector, structural-change and employment-rate terms; demographic and terms-of-trade terms; how the employment-rate term's weight changes with the horizon (WP08) |
| | Ladder of the working-age population | Everyone aged 15+ placed at their sector's output per worker, the non-employed at zero; dominance verdicts at two price bases, incidence curve, threshold indices (WP08) |
| | Data quality and coverage | Survey timeline, validation, model vs survey shares, grades |

### Data notes

- **Sectors.** 7 sectors (grid A) or 5 (grid B): UN value added exists for every country only at 7.
- **Price base.** Period decompositions default to initial-year prices (WP05's method); chained and final-year prices are one click away. Each country-period carries a verdict on whether its structural term agrees across the three (D-035); the note on the page explains how each treatment can fail.
- **Pooled aggregate.** Sums countries' value added and employment, so large economies dominate. In the LAC view Venezuela and Cuba are excluded by default (US$ levels not comparable); they can be added.
- **Survey coverage.** Survey years whose total employment is below 80% of ILO's national estimate (urban-only or partial surveys, e.g. Argentina) are not used for anchoring or as survey employment (D-031).
- **Latest year.** Sector data end in 2024, when UN value added ends. Labour-market series run to 2025 (ILO; later projections dropped).
- **Productivity measure.** Per worker in constant 2020 US$ by default; sector data are per worker. Per hour (ILO, 2021 PPP$) is available for whole-economy charts.

## Files

- `app.py`: navigation.
- `lib.py`: data loading, decomposition, chart helpers, and the palette (validated, colour-blind safe, one fixed colour per sector).
- `views/`: one file per page.
- Data come from `empirics/data/processed/<scope>/`, `empirics/data/interim/<scope>/ilo_labour.csv` (from `06_extract_labour.py`) and `empirics/output/<scope>/`, where `<scope>` is `lac_lp` or `carib_lp`. Both are built by the same pipeline in `empirics/code/lp/` with `LP_SCOPE=lac` or `LP_SCOPE=carib`.
