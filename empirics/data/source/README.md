# Source files kept in the repository

World-level source files that are small enough to commit and are shared by several empirical projects (D-029). Files here are stored exactly as downloaded, renamed only. Extracts and panels built from them live in `empirics/data/interim/` and `empirics/data/processed/`; larger raw files still go in `empirics/data/raw/`, which is not committed.

| File | Source | Vintage | Received | SHA-256 |
|---|---|---|---|---|
| `un_ama/un_ama_gdp_breakdown_constant2020_usd.xlsx` | UNSD National Accounts Main Aggregates, "GDP/breakdown at constant 2020 prices in US Dollars (all countries)" ([file 6](https://unstats.un.org/unsd/amaapi/api/file/6)) | January 2026 upload; 220 countries, 1970–2024 | 2026-11-09 | `49cae967082bcbef8b2f0e8a02d755a0809405bae82bc9a7cee4b010814d9e5c` |
| `un_ama/un_ama_gdp_breakdown_current_usd.xlsx` | UNSD AMA, "GDP/breakdown at current prices in US Dollars (all countries)" ([file 2](https://unstats.un.org/unsd/amaapi/api/file/2)) | Same | 2026-11-09 | `7cd48f2a282539d401bdf6c824e0f0271ff3b9c4648af43ec475da25e3828716` |

| `ilostat/EMP_2EMP_SEX_ECO_NB_A-20261109T1254.csv.gz` | ILOSTAT bulk download, employment by sex and economic activity, ILO modelled estimates, thousands ([bulk facility](https://ilostat.ilo.org/data/bulk/)) | Stamped 2026-11-09 12:54 UTC; all countries, 1991–2025 | 2026-11-09 | `5f48aa7491314ddcf253f57450af0dd0f55c6c994d3afd742a604b2bac48334d` |
| `ilostat/EMP_TEMP_SEX_ECO_NB_A-20261109T1254.csv.gz` | ILOSTAT bulk download, employment by sex and economic activity, national sources (surveys, censuses), thousands | Same stamp | 2026-11-09 | `2009f3868be6cbaffbcb57520718a5abb8c0b6d52b8cdbb169ac918e23f48383` |

Both UN files reproduce the committed Caribbean extracts (`interim/carib_lp/un_va_*.csv`) exactly (82 series checked, maximum relative difference 2e-16), so they are the vintage used for WP05.

Used by: `carib_lp` (WP05), the LAC extension of it, and the development-motors project.

The ILO files are a newer download (2026-11-09) than the one behind WP05 (2026-11-05). For the 16 Caribbean countries they are identical: every modelled value (34,020 rows) and every survey value (17,167 rows) is unchanged. The only difference is that ILO relabelled the source code of Haiti's 2012 survey from `BB:14099` to `BB:7725`, with the same values.
