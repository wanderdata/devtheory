# carib_lp: sectoral labour productivity for the Caribbean and for Latin America and the Caribbean

**Two scopes (D-030).** The same pipeline runs for the 16 Caribbean member States (`LP_SCOPE=carib`, the default; outputs in `.../carib_lp/`) and for the 33 Latin American and Caribbean member States of ECLAC (`LP_SCOPE=lac`; outputs in `.../lac_lp/`). The folder keeps its original name so that WP05's links stay valid. Raw inputs are the world files committed in `empirics/data/source/` (D-029).

Builds a country × sector × year panel of value added, employment and labour productivity for the 16 member countries of the ECLAC subregional headquarters for the Caribbean, for McMillan–Rodrik style decompositions (within-sector growth vs. structural change).

**Status (2026-11-05):** real files loaded (downloaded 2026-11-05: UN AMA upload of January 2026; ILO files stamped 20261105). Coverage report: [`empirics/output/carib_lp/coverage.md`](../../output/carib_lp/coverage.md). Decompositions for grids A and B run; method in [WP05 §2](../../../papers/WP05_caribbean_structural_change/WP05_caribbean_structural_change.md); results in [`results.md`](../../output/carib_lp/results.md).

## Countries (D-019)

Antigua and Barbuda, Bahamas, Barbados, Belize, Cuba, Dominica, Dominican Republic, Grenada, Guyana, Haiti, Jamaica, Saint Kitts and Nevis, Saint Lucia, Saint Vincent and the Grenadines, Suriname, Trinidad and Tobago. ECLAC's 13 Caribbean associate members (non-independent territories) are left out for now.

## Sources

| Key | Source | Use |
|---|---|---|
| `un_va_k2020_usd` | UNSD National Accounts Main Aggregates, GDP and its breakdown at constant 2020 prices in US$ ([file 6](https://unstats.un.org/unsd/amaapi/api/file/6)) | Real value added, 7 sectors |
| `un_va_cur_usd` | Same, current prices in US$ ([file 2](https://unstats.un.org/unsd/amaapi/api/file/2)) | Nominal shares, checks |
| `ilo_emp_model` | ILOSTAT `EMP_2EMP_SEX_ECO_NB_A`, ILO modelled estimates (thousands) | Employment, balanced annual series |
| `ilo_emp_survey` | ILOSTAT `EMP_TEMP_SEX_ECO_NB_A`, national sources (thousands) | Employment, actual survey/census years; robustness |

The two employment series are kept side by side (D-021): the modelled series is complete but interpolated where surveys are missing, which smooths employment shares and biases the structural change term toward zero.

## Sectors (D-020)

The UN AMA's seven groupings (ISIC Rev.3): AGR agriculture (A–B); MIU mining and utilities (C, E; derived as C–E minus D); MAN manufacturing (D); CON construction (F); TRH trade, restaurants and hotels (G–H); TSC transport, storage and communication (I); OTH other services (J–P). ILO employment in ISIC Rev.4 is mapped in `concordance.py`; the approximations (ISIC4 J and E) are documented there.

## Data-quality rules (D-023)

- Constant-price mining+utilities = current-price (C–E minus D) × C–E deflator, not the constant-price residual (which goes negative under chain-linking).
- Survey country-years with more than 25% of workers unclassified are dropped.
- Survey years missing any of the 7 sectors are not used; missing ISIC sections in used years are reported in the coverage file.
- Survey years whose total employment is below 80% of the ILO modelled national total are treated as not national (urban-only or partial surveys) and not used (D-031).

## Price bases (D-024, D-032)

`05_decompose.py` writes each period decomposition at initial-year prices (`main.csv`), final-year prices (`robust_final_prices.csv`) and chained prices (`robust_chained.csv`: one decomposition per year at previous-year prices, averaged over the period), plus excluding-mining variants for each. The dashboard lets the user switch between them; initial-year is its default, and each country-period gets a verdict on agreement across the three (D-035). Chained results can suffer chain drift where annual employment shares are noisy. `07_lac_summary.py` (LAC scope only) writes the regional summary tables and figures for WP06 to `empirics/output/lac_lp/summary/`.

## Running it

Prefix any step with `LP_SCOPE=lac` for the LAC scope.

```
python empirics/code/carib_lp/01_download.py      # needs access to unstats.un.org and rplumber.ilo.org
python empirics/code/carib_lp/02_extract.py [files...]   # raw world files -> 16-country extracts
python empirics/code/carib_lp/03_build_panel.py    # extracts -> panel + coverage report
python empirics/code/carib_lp/03b_build_panel5.py  # grid B (5-sector) employment
python empirics/code/carib_lp/04_validate.py       # modelled vs survey employment
python empirics/code/carib_lp/05_decompose.py      # decompositions, both grids
python empirics/code/carib_lp/06_extract_labour.py # ILO labour-market series for the dashboard
streamlit run empirics/dashboard/app.py            # dashboard (see empirics/dashboard/README.md)
```

`02_extract.py` recognises files by content, so downloads can keep their original names and be passed as arguments.

## Where things go

| Path | Contents | Committed |
|---|---|---|
| `empirics/data/raw/carib_lp/` | World files as downloaded | No (large; re-downloadable) |
| `empirics/data/interim/carib_lp/` | 16-country extracts + `sources.csv` | Yes |
| `empirics/data/processed/carib_lp/` | `panel_7sector.csv`, `emp_all_sources.csv` | Yes |
| `empirics/output/carib_lp/` | `coverage.md`, `coverage.csv` | Yes |

## Units

UN value added is in US dollars as published (check the file header for scale); ILO employment is in thousands. `lp_*` columns are US dollars (constant 2020) per person employed.
