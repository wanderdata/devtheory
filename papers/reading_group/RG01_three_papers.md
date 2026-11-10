# RG01 — Three papers beyond sector shares

*Paul Wander · devtheory reading and replication series · 10 November 2026 · status: selection, not yet read in full*

## Why these three

WP07 tested whether a sector's share of GDP predicts growth and found that, since 1990, none robustly does except agriculture. I drew three lessons from it (research log, session 17):

1. The **unit** is wrong: productivity differences within a sector are larger than those between sectors.
2. Shares are **outcomes**, so a regression of growth on them cannot identify a cause.
3. A "motor" **bundles mechanisms**: productivity level and growth, linkages, learning, jobs and foreign exchange.

Each paper below attacks one of these. Together they span three levels the programme needs: activities with a credible causal design, firms within a sector, and jobs.

Selection criteria, fixed before choosing:

- published 2023 or later in a peer-reviewed outlet;
- addresses at least one of the three lessons;
- has a design we can either reproduce or re-run on LAC data available to us;
- has a clear LAC counterpart.

Papers already digested in earlier work were not eligible: Kruse et al. (L115, used in WP07); Fan, Peters & Zilibotti (L128); Alfaro-Ureña, Manelici & Vasquez (L092, used in WP03); Rodrik & Sandhu (L049).

| | Paper | Lesson it attacks | Level | Replication route |
|---|---|---|---|---|
| 1 | Lane (2025), *Manufacturing Revolutions*, QJE 140(3) | Causality; mechanisms (linkages, dynamic comparative advantage) | Activities (industries) | Reproduce if the package is public; re-run the design on Brazil's II PND |
| 2 | Diao, Ellis, McMillan & Rodrik (2025), *Africa's Manufacturing Puzzle*, WBER 39(2) | Unit; mechanisms (productivity vs jobs) | Firms by size within a sector | Original microdata restricted; re-run the method on Mexico's economic censuses |
| 3 | Donovan, Lu & Schoellman (2023), *Labor Market Dynamics and Development*, QJE 138(4) | Unit (jobs); mechanisms (learning, job quality) | Jobs and workers | Public replication package (Harvard Dataverse); extend with Mexico's ENOE panel |

---

## 1. Lane (2025): can a policy-driven expansion of an activity cause lasting growth?

**Citation.** Lane, N. (2025). "Manufacturing Revolutions: Industrial Policy and Industrialization in South Korea." *Quarterly Journal of Economics* 140(3): 1683–1741. doi:10.1093/qje/qjaf025. Working-paper version: arXiv:2505.20566.

**What it does.** Korea's heavy and chemical industry (HCI) drive, 1973–79, targeted six groups: steel, nonferrous metals, shipbuilding, machinery, electronics and petrochemicals. The paper compares targeted with non-targeted manufacturing industries before, during and after the drive, using a dynamic difference-in-differences relative to 1972. The drive's end (Park's assassination in 1979) lets it test persistence. Robustness comes from a doubly robust DiD and a cross-country triple difference.

Data:
- digitised Mining and Manufacturing Survey panels (four-digit, 1967–86; five-digit, 1970–86);
- the Bank of Korea's 1970 input–output table (about 320 sectors);
- UN Comtrade trade flows;
- tariff and quota measures.

**Headline results**, from the arXiv introduction; to be re-checked against the published version:
- targeted industries' output rose by more than 100% relative to the controls;
- their labour productivity rose by more than 15%;
- they were about 10 points more likely to gain revealed comparative advantage;
- downstream users of targeted inputs also gained, through the input–output network;
- the gains persisted after 1979, and some appeared only with a lag.

**Why it matters here.** It is the cleanest answer to the question WP07 could not ask: does *exogenously* expanding an activity raise its productivity and that of its users? It also separates two mechanisms that the "manufacturing motor" bundles: the activity's own learning (dynamic comparative advantage) and its linkages to other activities.

**Replication.**
- (a) *Reproduce.* QJE requires a replication package, normally on its Harvard Dataverse. I could not confirm one from here: the workspace cannot reach Dataverse, and RePEc lists none. If it exists, the user downloads it, and we re-estimate the event-study figures in Python and compare.
- (b) *LAC twin.* Brazil's Second National Development Plan (II PND, 1974–79) targeted capital goods and basic inputs (steel, nonferrous metals, petrochemicals, fertilisers, pulp and paper) in the same years, under a similar oil shock. That gives a near-natural comparison. *(The list of sectors is from memory and must be checked against primary sources.)* Data:
  - IBGE industrial censuses for 1970, 1975, 1980 and 1985 by industry;
  - a Brazilian input–output table for the 1970s;
  - SITC trade data from 1962, such as the Growth Lab's Atlas files.
- (c) *Cheap first step.* Revealed-comparative-advantage event studies for Korea and Brazil from SITC data alone. This tests whether targeted products gained RCA in both countries, or only in Korea.

**LAC proposition (P-RG1).** Brazil's II PND raised targeted industries' output, but their productivity and revealed comparative advantage rose less than Korea's, and the downstream gains were smaller.
- *Support:* DiD output effects comparable to Korea's, with productivity and RCA effects near zero or not persistent after 1985.
- *Rejection:* productivity and RCA effects of similar size to Korea's. That would shift the explanation of the two countries' divergence away from the policy's design and toward what came after: the debt crisis and macroeconomic instability.

Either result informs Q3 of WP07 (why the motor works only in some contexts) with a design rather than an interaction term.

**Questions for our reading.**
- How does the paper rule out that planners picked industries already about to take off?
- How large are the downstream effects relative to the direct ones?
- What does the cross-country triple difference use as foreign placebo sectors?

---

## 2. Diao, Ellis, McMillan & Rodrik (2025): who in a sector produces productivity, and who produces jobs?

**Citation.** Diao, X., Ellis, M., McMillan, M. & Rodrik, D. (2025). "Africa's Manufacturing Puzzle: Evidence from Tanzanian and Ethiopian Firms." *World Bank Economic Review* 39(2): 308–340. doi:10.1093/wber/lhae029. Working paper: NBER WP 28344 (2021); the earlier version is L051.

**What it does.** In Africa's recent growth accelerations, labour left agriculture but productivity in the modern sectors fell. The paper uses new firm-level panels (Tanzania 2008–16; Ethiopia 1996–2017) and splits manufacturing by firm size. It finds a dichotomy:
- larger firms raise productivity but add few jobs;
- small firms absorb labour with no productivity growth;
- large firms use far more capital-intensive techniques than their countries' income or factor endowments would predict.

The authors link that to globally determined technology.

**Why it matters here.** It is the most direct evidence for lesson 1: the "manufacturing" average hides two activities with opposite properties. It also maps onto our proposition P3, that no activity scores high on both labour absorption and dynamism. If the dichotomy holds within sectors, the useful unit is sector × size (or formality), not the sector. That is the same unit as OQ-46.

**Replication.**
- (a) *Reproduce.* Not feasible. The Tanzanian and Ethiopian microdata come from the national statistical offices under agreements.
- (b) *LAC re-run of the method.* Mexico's economic censuses (1999, 2004, 2009, 2014, 2019) publish employment, gross value added, remuneration and fixed assets by detailed industry and establishment size class. That is enough for the paper's core exercises at size-class level: productivity and employment growth by size, a shift-share split into within-size and between-size terms, and capital intensity by size relative to income. Two features make Mexico a stronger test than Africa:
  - the censuses cover services as well as manufacturing, so we can ask Rodrik and Sandhu's question about labour-absorbing services;
  - Mexico's informal establishments are in the census, so small and informal can be partly separated.

  Chile's ENIA and Colombia's EAM could follow, but they cover formal plants only.
- *Caveat.* With size-class tabulations we cannot follow firms across classes, so "small firms do not grow" cannot be told apart from "successful small firms graduate out of the class". The paper's firm panels can. The census microdata can too, but only in INEGI's on-site laboratory.

**LAC proposition (P-RG2).** In Mexico 1999–2019, establishments with 50 or more workers account for most of manufacturing's labour-productivity growth, and establishments with 10 or fewer for most of its employment growth. The same split holds in retail and personal services.
- *Rejection:* large establishments contributing a share of employment growth at least equal to their initial employment share, or small establishments showing productivity growth comparable to large ones.

The prior from Levy (2018, *Under-Rewarded Efforts*, from memory) is that Mexico's split is, if anything, sharper than Africa's.

**Questions for our reading.**
- How do the authors define size classes, and how sensitive is the dichotomy to the cut-off?
- How much of the small-firm stagnation is selection (graduates leaving the class)?
- Is the capital-intensity finding about technology choice or relative prices (cheap capital for large firms)?

---

## 3. Donovan, Lu & Schoellman (2023): which jobs are rungs on a ladder?

**Citation.** Donovan, K., Lu, W.J. & Schoellman, T. (2023). "Labor Market Dynamics and Development." *Quarterly Journal of Economics* 138(4): 2287–2325. doi:10.1093/qje/qjad019. Replication package: Harvard Dataverse, doi:10.7910/DVN/RXWKTV (dated 2023-05-15).

**What it does.** The paper harmonises rotating-panel labour force surveys covering about 80 million people in 49 countries. It shows that flows such as job finding and employment exit are much higher in poorer countries. The authors attribute this to a "slippery job ladder": workers move often into and out of marginal jobs and rarely reach, or stay in, better-paid ones. Subsistence self-employment and selection into wage work also contribute.

**Why it matters here.** It moves the unit to the job and gives "motor" a measurable worker-side meaning. A job is a rung if it lasts and leads to better jobs; a dead end if it churns. That covers the learning and job-quality mechanisms that a sector share cannot see. Latin American surveys are well suited to this: Mexico's ENOE, Brazil's PNAD Contínua, Argentina's EPH and Chile's ENE all have rotating panels.

**Replication.**
- (a) *Reproduce.* Feasible. The package is public. The README will say whether the harmonised microdata are included or must be rebuilt from national surveys. The workspace cannot reach Dataverse, so the user downloads it.
- (b) *Extend.* Re-estimate the flows by **sector × firm size × formality** for Mexico (ENOE records firm size and social-security status). Then ask which kinds of job have low exit rates and high transition rates into better-paid jobs a year later. This is the job-level counterpart to paper 2 and the empirical core of OQ-46.

**LAC proposition (P-RG3).** In Mexico, firm size and formality explain more of the variation in job exit rates and upward transitions than sector does.
- *Support:* in a decomposition of flow rates, the size × formality cells account for a larger share of between-cell variance than the 1-digit sector.
- *Rejection:* sector dominates, or manufacturing jobs are better rungs than service jobs at the same size and formality. That would partly rehabilitate the sector as a unit, for the job-quality mechanism.

**Questions for our reading.**
- How do the authors separate true flows from measurement error in survey-reported status, a known problem in rotating panels?
- Which LAC countries are in the 49?
- Does the slippery ladder vary with firm size in their data, or only with employment status?

---

## What we will do with them

1. **Read in full.** The working-paper versions are open: arXiv 2505.20566 for Lane, NBER WP 28344 for the Africa paper and Minneapolis Fed Staff Report 596 for Donovan et al. I can read those here. The published versions are paywalled; if the user has them, attaching the PDFs lets us check that the numbers match. Each reading produces a one-page note: question, design, main estimates with page references, the identifying assumption in one sentence, and what would break it. The literature register is updated to *verified* only for claims checked against the text.
2. **Replicate in order of feasibility.**
   - Paper 3, from its package.
   - Paper 2's method on Mexico's census tabulations.
   - Paper 1, starting with its RCA event studies, which need only trade data, before attempting the Brazilian industrial censuses.
3. **Pre-register the LAC propositions** above, as in D-037, before touching LAC data.
4. **Display.** If at least two replications succeed, a third app (`apps/beyond_sectors/`) shows each paper's original result next to its LAC counterpart.

### Data the user would need to download

| For | File | Where |
|---|---|---|
| Paper 3 | Replication package | Harvard Dataverse, doi:10.7910/DVN/RXWKTV |
| Paper 3, extension | ENOE microdata, a few quarters (e.g. 2019 and 2023) | INEGI, *Microdatos* |
| Paper 2, LAC | Economic census results by industry and establishment size, 1999–2019 | INEGI, *Censos Económicos*, SAIC |
| Paper 1 | Replication package, if one exists | QJE Dataverse |
| Paper 1, RCA step | SITC rev. 2 trade by country and product, from 1962 | Growth Lab, Atlas of Economic Complexity data (Harvard Dataverse) |

### Near misses

These were left out, not rejected:

- Kremer, Willis & You (2022, *NBER Macroeconomics Annual*), on the post-1995 convergence of growth correlates. Highly relevant to WP07's method, but it is a critique of cross-country regressions rather than a new unit of analysis.
- Eslava, Haltiwanger & Urdaneta (2024, *Review of Economic Studies*), on Colombian plants' life cycles: a LAC firm paper, but on restricted DANE microdata.
- Huneeus & Rogerson (2024, *Review of Economic Studies*), on heterogeneous paths of industrialisation.

The three citations in this list are from memory and are to be verified before use.
