# Testable propositions (v0.1, 2026-11-02)

Each proposition states the claim, which idea it comes from, what would support or reject it, and candidate data for Phase 2. Numbering is permanent; revisions are logged in `docs/register/decision_log.md`.

| # | Proposition | Idea | Support if… | Reject if… | Candidate data |
|---|---|---|---|---|---|
| P1 | In LAC, the between-segment, within-industry term accounts for a larger share of the gap in labor-productivity growth than the between-industry term. | 1 | three-way decomposition shows large negative middle term | middle term small relative to between-industry term | household surveys (SEDLAC harmonized; EPH, PNAD, ENOE, CASEN, GEIH) linked to national accounts; GGDC/ETD sector data |
| P2 | Post-1990 "growth-reducing structural change" in LAC is mostly movement into the $T$ segment of services, not into services as such. | 1 | $M$-segment services have productivity ≥ economy average; flows went to $T$ services | services' $M$ segment also below average | same as P1 |
| P3 | No activity in contemporary LAC scores high on all five properties (L, D, A, T, C); the correlation between Absorption and Dynamism across activities is negative today but was ~0 or positive for manufacturing in 1960–80 East Asia. | 2 | negative A–D correlation now; weaker or positive historically | strong positive A–D correlation for some LAC activities | sector × segment panels; UNIDO INDSTAT; ETD; historical Korea/Taiwan data |
| P4 | Experience-wage slopes are steeper in $M$ than $T$ jobs, conditional on industry, education and cohort. | 3 | significant slope gap | no gap after controls | household surveys (pseudo-panels); RAIS (Brazil), IMSS (Mexico), Chile admin data |
| P5 | Workers moving $T \to M$ experience a change in wage *growth*, not only a level jump (rules out pure selection). | 3 | slope change in within-worker event studies | only level change | panel/administrative data with informal spells (Brazil PNAD-C rotating panel, Mexico ENOE panel) |
| P6 | Founders of growing firms disproportionately come from prior employment in large/$M$ firms. | 3, 4 | strong association in employer–employee data | no association | RAIS; Chile; Colombia PILA |
| P7 | Commodity booms reduce tradable $M$ employment and raise $T$ services employment, and the reversal in busts is incomplete (asymmetric hysteresis). | 4 (loop 3) | asymmetric responses to commodity price shocks | symmetric responses | country/region panels with commodity price shocks; Bartik exposure by subnational region |
| P8 | Larger gaps between contributory and non-contributory benefits raise $T$ shares, especially in sectors with many small firms. | 4 (loop 2) | expansions of non-contributory programs raise informality | no effect | program rollouts (e.g., Seguro Popular, Bolsa Família, Chile's pensions reform) |
| P9 | Within-firm productivity growth is lower in more concentrated industries in LAC, and the effect is stronger than in comparator regions. | 4 (loop 4) | negative concentration–productivity-growth link | none | firm censuses/surveys (ENIA Chile, EAM Colombia, PIA Brazil, Mexico economic census) |
| P10 | Productivity-raising entry of $M$ firms in non-tradable services raises sector productivity but has a small or negative effect on aggregate productivity in regions with weak tradable income growth; the effect is positive where tradable income grows. | 5 | interaction between local tradable income growth and services upgrading | no interaction | supermarket/chain entry; regional accounts; employer data |
| P11 | LAC's shortfall relative to the post-2000 convergence trend is accounted for mainly by within-segment productivity of $M$ firms and the low $M$ employment share, not by factor accumulation. | 1–4 | decomposition | factor accumulation dominates | PWT; ETD; IMF/IDB firm data |
| P12 | Resource-based activities with dense domestic supplier linkages score higher on C and A than enclave resource activities. | 2 | linkage density predicts supplier productivity and employment | no difference | input–output tables (OECD TiVA, national IO), mining supplier programs (Chile) |

## Priority for Phase 2

P1–P2 (core reconciliation), P4–P5 (core of Idea 3), P7 (most distinctive LAC mechanism). P3 needs a measurement design first.

## Propositions from WP02–WP04 (added 2026-11-02/03)

| # | Proposition | Source | Candidate data |
|---|---|---|---|
| P13 | Informality falls mainly through new cohorts entering formal jobs, not incumbents formalizing | WP02 | household-survey panels |
| P14 | Wider contributory/non-contributory benefit gaps raise informality mostly among small salaried employers | WP02 | program rollouts |
| P15 | Firm-size bunching below enforcement and tax thresholds | WP02 | economic censuses |
| P16 | Higher informal share predicts slower productivity growth of formal firms in the same market | WP02 | census panels |
| P17 | Domestic suppliers to MNCs gain persistently in employment, productivity and sales to others | WP03 | firm-to-firm data |
| P18 | Horizontal spillovers from foreign entry: zero/negative on productivity, positive on prices | WP03 | entry events |
| P19 | FDI income from domestic-market sectors tightens external constraints | WP03 | BoP primary income |
| P20 | Effective tax rates on foreign affiliates fall with intra-firm fees and royalties | WP03 | tax/firm data |
| P21 | Payroll-financed transfers raise informality more where the formal base is already small (nonlinear) | WP04 E3 | country/state panels |
| P22 | Formal take-offs follow large or permanent changes (wedge reform, large sustained export expansion), not small/temporary ones | WP04 E4 | growth-episode data |
| P23 | Commodity booms cause lasting tradable declines only near the threshold; weaker where rents are saved or cut taxes on formal labor | WP04 E5 (refines P7) | subnational shocks × initial formality |
| P24 | Managerial supply raises formal employment persistently only where tradable productivity is also rising | WP04 E1/E4 | regional panels |

## Propositions on defining and measuring productive development (added 2026-11-12)

See `03_defining_productive_development.md` and WP08. Numbering continues from P24.

| # | Proposition | Source | Support if… | Reject if… | Data |
|---|---|---|---|---|---|
| P25 | The employment-rate term's weight in the growth of output per working-age person falls with the horizon; over 20 years productivity accounts for nearly all of it. | 03, WP08 | employment-rate share of variance falls from short to long windows (first pass, LAC: 27% at 1 year, 8% at 20) | the share is similar at all horizons | UN AMA, ILO modelled estimates (in hand) |
| P26 | Sector-level ladder verdicts change once sectors are split by formality and firm size: more country-periods become ambiguous or deteriorations, because low-productivity segments grew within sectors that look stable at sector level. | 03, WP08; P1–P2 | in Mexico, the verdict for 2005–2019 or 2005–2023 with sector × formality × size steps differs from the sector-only verdict | verdicts unchanged | INEGI informal-economy accounts; economic censuses; ENOE | Mexico result (2026-11-13, WP09 study 9.3): **rejected for Mexico**; no verdict changes in four periods under any of seven specifications (θ 0.5–2, medians, size split). |
| P27 | Part of the rise in low-productivity services' relative productivity at current prices is a rise in their relative prices (Baumol), and relative prices offset part, not all, of differences in real productivity growth across sectors. | 03, WP08 | slope of relative-price change on real relative-productivity change between −1 and 0 and significantly below 0 | slope near 0, or near −1 | UN AMA current and constant prices, ILO (in hand) |

## Propositions on jobs in Mexico (WP09, added 2026-11-13)

| # | Proposition | Source | Support if… | Reject if… | Status |
|---|---|---|---|---|---|
| P28 | Experience–earnings profiles are much steeper in formal than in informal wage jobs, and differences by formality are larger than differences across sectors. | WP09 study 9.2 | formal height at 20–24 years ≥ 1.5 × informal, and the formal–informal gap exceeds the range across six sector groups | ratio < 1.2, or the sector range exceeds the gap | **Rejected** (2026-11-13): ratio 1.6, but sector range 21 points > formality gap 10 points; within manufacturing and commerce formal ≈ informal |
| P29 | A substantial part of the flatness of Mexico's national profile reflects the type of job held at each level of experience. | WP09 study 9.2 | composition term ≥ a third of (national − formal) | < 10% | **Rejected** (2026-11-13): composition steepens the national profile (+0.038 log points); national ≈ formal |
| P30 | Within-sector reallocation between formal and informal work is a material part of Mexico's within-sector productivity term. | WP09 study 9.3; P1–P2 | for 2005–2019, the between-segment term within sectors is at least a quarter of the sector-level within term in absolute value | less than a tenth | **Supported narrowly, not robust** (2026-11-13): +0.071 pp a year against a within term of −0.268 (26%) at θ = 1; 13% at θ = 0.5, 21% with medians, 10% with the size split, 52% at θ = 2. In 2005–2008 formalisation accounts for the whole sector-level within gain. |
| P31 | The 2019 border package (minimum wage doubled, VAT and income tax cut) raised low wages without reducing employment. | WP09 study 9.4 | log hourly earnings of wage employees rise (90% interval > 0), employment-rate interval excludes −1.5 pp, and excess jobs above the new minimum ≥ 0.7 × missing jobs below | employment rate falls ≥ 1 pp (interval < 0), or earnings effect < 2% and not significant | **Inconclusive** (2026-11-13): employment rate +0.9 pp (−0.1 to +1.8); earnings measures fail the plan's §6 checks (pre-trends; reporting fell 7.8 pp in the zone); excess/missing 0.59 |
| P32 | The package increased quarterly moves from informal to formal work in the border zone. | WP09 study 9.4 | effect on the informal→formal rate > 0 (90% interval) and formal employment rate does not fall | 90% interval excludes +10% of the pre-period rate | **Rejected, narrowly** (2026-11-13): −1.2 pp a quarter (−5.0 to +1.6) against a pre-period rate of 18.5% |
| P33 | The new minimum moved informal wages too (lighthouse effect): informal jobs paying below it fell. | WP09 study 9.4 | sum of effects in informal bins below the minimum < 0 (90% interval) | interval excludes a fall of a quarter of the pre-period mass | **Inconclusive** (2026-11-13): informal jobs below the minimum −0.8 per 100 people 15+ (−1.6 to −0.1), but informal non-reporters +1.1 and no informal excess jobs; bins unreliable under §6 |
| P34 | First jobs (self-reported, ages 15–24) are more informal than young people's jobs in general. | WP09 study 9.5 | informal share of first jobs exceeds that of all employed 15–24 by ≥ 10 pp | < 3 pp | **Supported** (2026-11-13): 85.1% of first jobs informal against 68.5% of all jobs of employed 15–24 |
| P35 | Informal first jobs are stepping stones: never-worked young people who take an informal job are later more often formal than comparable young people still not employed. | WP09 study 9.5 | difference in formal employment three quarters later > 0 (90% interval) | 90% interval < 0 (trap) | **Supported** (2026-11-13): +3.4 pp (3.0–3.7) on a base of 2.5%; Oster delta 14.6; larger with ≥ 12 years of schooling (+6.0) |
| P36 | The formality of the first job persists: formal entrants are ≥ 25 pp more likely than informal entrants to be formal three quarters later, conditional on observables. | WP09 study 9.5 | lower 90% bound ≥ 25 pp | upper bound < 25 pp | **Supported** (2026-11-13): +34.0 pp (32.3–35.8); probit 27.5; Oster delta 3.2 (0.9 with Rmax = 2 × R²) |
| P37 | Among informal first jobs, wage jobs in units with premises lead to formal work more often than own-account or unpaid work. | WP09 study 9.5; 9.1 | ≥ 10 pp with 90% interval > 0 | upper bound < 10 pp | **Rejected** (2026-11-13): +4.2 pp (3.4–5.0) on a base of 3.9%: positive in every sample but below the 10-point threshold |
| P38 | States differ in one-year informal-to-formal mobility beyond composition and sampling error. | WP09 study 9.6 | signal variance ≥ ½ of the variance of estimated state effects (2005–2011) | < ⅕ | Open |
| P39 | State differences in mobility persist between 2005–2011 and 2012–2018. | WP09 study 9.6 | disattenuated correlation ≥ 0.5 | < 0.2 | Open |
| P40 | States with more informal-to-formal mobility in 2005–2011 grew faster in GDP per person in 2012–2019. | WP09 study 9.6 | Spearman correlation > 0 (90% bootstrap interval, 30 states without Campeche and Tabasco) | interval < 0 | Open |
