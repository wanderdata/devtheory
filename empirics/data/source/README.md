# Source files kept in the repository

World-level source files that are small enough to commit and are shared by several empirical projects (D-029). Files here are stored exactly as downloaded, renamed only. Extracts and panels built from them live in `empirics/data/interim/` and `empirics/data/processed/`; larger raw files still go in `empirics/data/raw/`, which is not committed.

| File | Source | Vintage | Received | SHA-256 |
|---|---|---|---|---|
| `un_ama/un_ama_gdp_breakdown_constant2020_usd.xlsx` | UNSD National Accounts Main Aggregates, "GDP/breakdown at constant 2020 prices in US Dollars (all countries)" ([file 6](https://unstats.un.org/unsd/amaapi/api/file/6)) | January 2026 upload; 220 countries, 1970–2024 | 2026-11-09 | `49cae967082bcbef8b2f0e8a02d755a0809405bae82bc9a7cee4b010814d9e5c` |
| `un_ama/un_ama_gdp_breakdown_current_usd.xlsx` | UNSD AMA, "GDP/breakdown at current prices in US Dollars (all countries)" ([file 2](https://unstats.un.org/unsd/amaapi/api/file/2)) | Same | 2026-11-09 | `7cd48f2a282539d401bdf6c824e0f0271ff3b9c4648af43ec475da25e3828716` |
| `ilostat/EMP_2EMP_SEX_ECO_NB_A-20261109T1254.csv.gz` | ILOSTAT bulk download, employment by sex and economic activity, ILO modelled estimates, thousands ([bulk facility](https://ilostat.ilo.org/data/bulk/)) | Stamped 2026-11-09 12:54 UTC; all countries, 1991–2025 | 2026-11-09 | `5f48aa7491314ddcf253f57450af0dd0f55c6c994d3afd742a604b2bac48334d` |
| `ilostat/EMP_TEMP_SEX_ECO_NB_A-20261109T1254.csv.gz` | ILOSTAT bulk download, employment by sex and economic activity, national sources (surveys, censuses), thousands | Same stamp | 2026-11-09 | `2009f3868be6cbaffbcb57520718a5abb8c0b6d52b8cdbb169ac918e23f48383` |
| `ilostat/EMP_2WAP_SEX_AGE_RT_A-20261109T1259.csv.gz` | ILOSTAT bulk download, employment-to-population ratio (%), ILO modelled estimates | Stamped 2026-11-09 12:59 UTC | 2026-11-09 | `24ee16170e456f5e56f5da3c52a661dc4b47068af005bb47db9993e2beef2971` |
| `ilostat/EAP_2WAP_SEX_AGE_RT_A-20261109T1259.csv.gz` | ILOSTAT bulk download, labour force participation rate (%), ILO modelled estimates | Stamped 2026-11-09 12:59 UTC | 2026-11-09 | `e61ada2f71828cafe99f4e8add5ed3681e579fc8e2faca7dd0af7a66246950ee` |
| `ilostat/UNE_2EAP_SEX_AGE_RT_A-20261109T1259.csv.gz` | ILOSTAT bulk download, unemployment rate (%), ILO modelled estimates | Stamped 2026-11-09 12:59 UTC | 2026-11-09 | `798a48432590eaedde9e4986a5723bf280cf8641e5f52621f3c713facfe7778b` |
| `ilostat/GDP_2HRW_NOC_NB_A-20261109T1259.csv.gz` | ILOSTAT bulk download, output per hour worked (GDP, constant 2021 PPP $), ILO modelled estimates | Stamped 2026-11-09 12:59 UTC | 2026-11-09 | `e731f3f7fd4e856f09dee69ec7c865980dbc93b1dc0d00418dc74397d990de5d` |
| `ilostat/HOW_2EMP_SEX_NB_A-20261109T1259.csv.gz` | ILOSTAT bulk download, mean weekly hours actually worked per employed person, ILO modelled estimates | Stamped 2026-11-09 12:59 UTC | 2026-11-09 | `ca4a80846730dd9de56e6184c1c65a235ffa52394c6650facfc8ed752362fd26` |
| `pwt/pwt110.xlsx` | Penn World Table 11.0 ([PWT 11.0](https://www.rug.nl/ggdc/productivity/pwt/pwt-releases/pwt110)); real GDP, population, employment, human capital, capital, price levels | 185 countries, 1950–2023 | 2026-11-09 | `7b337e94f39dfe304bc459e433f8ce0624496c812707ae0c924888f5142b3ab3` |
| `ggdc/ETD_230918.xlsx` | GGDC/UNU-WIDER Economic Transformation Database ([ETD](https://www.rug.nl/ggdc/structuralchange/etd/)); value added (current and constant 2015 local currency) and persons engaged, 12 sectors (ISIC Rev. 4) | Release of 15 July 2021 (file dated 2023-09-18); 51 countries, 1990–2018 | 2026-11-09 | `00ab35e3e9349834238b4d23c52dd3d46f7a7e7b22538b7db988a1bf78630df5` |
| `ggdc/10sd_jan15_2014.xlsx` | GGDC 10-Sector Database ([structural change databases](https://www.rug.nl/ggdc/structuralchange/)); value added (current and constant national prices) and persons engaged, 10 sectors (ISIC Rev. 3.1) | January 2015 release; 42 countries (plus an alternative Nigeria series), 1947–2013, start dates vary | 2026-11-09 | `0a99de029c82fef8e68d7841c93a7ec1b9671f0b5e59c7094d0bbbab61c08e24` |

Both UN files reproduce the committed Caribbean extracts (`interim/carib_lp/un_va_*.csv`) exactly (82 series checked, maximum relative difference 2e-16), so they are the vintage used for WP05.

Used by: `carib_lp` (WP05), the LAC extension of it, and the development-motors project.

The ILO files are a newer download (2026-11-09) than the one behind WP05 (2026-11-05). For the 16 Caribbean countries they are identical: every modelled value (34,020 rows) and every survey value (17,167 rows) is unchanged. The only difference is that ILO relabelled the source code of Haiti's 2012 survey from `BB:14099` to `BB:7725`, with the same values.

The five ILO labour-market series (rates, output per hour, hours) reproduce the Caribbean extract used by the dashboard exactly.

## Licences and attribution

Each source permits redistribution with attribution; cite the source wherever its data are shown (the apps' footers and the papers' source notes do).

| Source | Terms | Checked |
|---|---|---|
| UN Statistics Division (UNdata), National Accounts Main Aggregates | Free to use, copy, reproduce and redistribute; UNdata must be cited as the source ([conditions of use](https://data.un.org/Host.aspx?Content=UNdataUse)) | 2026-11-09 |
| ILO, ILOSTAT | Datasets published from 3 May 2023 are licensed CC BY 4.0, with credit to the ILO ([rights and permissions](https://www.ilo.org/node/9321)) | 2026-11-09 |
| Penn World Table 11.0 | CC BY 4.0; cite Feenstra, Inklaar and Timmer (2015), *American Economic Review* 105(10) ([PWT 11.0 page](https://www.rug.nl/ggdc/productivity/pwt/pwt-releases/pwt110)) | 2026-11-09 |
| GGDC/UNU-WIDER ETD | The file asks users to cite de Vries et al. (2021), "The Economic Transformation Database (ETD): content, sources, and methods", WIDER Technical Note 2021/2; no licence is stated in the file. Treated as redistributable with citation, as published on the GGDC site | 2026-11-09 |
| GGDC 10-Sector Database | Cite Timmer, de Vries and de Vries (2015), "Patterns of Structural Change in Developing Countries", in *Routledge Handbook of Industry and Development*; no licence is stated in the file | 2026-11-09 |

Used by WP07 (development motors): PWT, ETD, GGDC 10-Sector. ETD and the 10-Sector database do not state a licence; if either is ever found to restrict redistribution, move it to `raw/` and keep only the checksum here.
