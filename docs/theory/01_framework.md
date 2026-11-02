# Conceptual framework (v0.1, 2026-11-02)

This is a working draft. It states the framework's building blocks and five ideas that refine the standard account, each tied to the tension in the literature it resolves (`docs/literature/00_synthesis.md`). Testable implications are collected in `02_propositions.md`.

---

## 0. Starting point: what the standard account gets right

1. Long-run income differences are mostly productivity differences (strand 1).
2. Productivity rises both within activities (adoption, learning, management, scale) and through reallocation toward more productive activities (strand 2).
3. Historically, the fastest catch-up combined both at once, through labor-intensive, tradable manufacturing (strand 3; East Asia).
4. LAC's problem is low and stagnant TFP, with large misallocation, a mass of micro and informal units, early deindustrialization, and commodity-driven volatility (strands 4 and 7).

What the standard account does not do well: (a) it uses *sectors* as the unit of structural change and *firms* as the unit of misallocation, and the two never meet; (b) it treats "good jobs" as a welfare concept rather than a growth concept; (c) it is mostly static; (d) it lacks an explanation of persistence; (e) it ignores the demand side of labor absorption.

---

## 1. Building blocks and notation

Let the economy have industries $s = 1,\dots,S$ and, within each industry, **segments** $m \in \{M, T\}$: a modern segment $M$ (formal, organized, firms with internal hierarchies, typically ≥ some size) and a traditional segment $T$ (informal, own-account and micro units). The segment boundary is an empirical object (see D-005); the binary split is a simplification of a continuum indexed by firm size and formality.

Aggregate labor productivity:

$$
y = \sum_{s}\sum_{m} \ell_{sm}\, y_{sm}, \qquad \ell_{sm} = L_{sm}/L .
$$

Three-way decomposition of productivity growth between $t-k$ and $t$:

$$
\Delta y = \underbrace{\sum_{s,m} \ell_{sm,t-k}\,\Delta y_{sm}}_{\text{within segment}}
+ \underbrace{\sum_{s}\sum_{m} \big(\Delta \ell_{sm} - \tfrac{\ell_{sm}}{\ell_s}\Delta\ell_s\big)\, y_{sm}}_{\text{between segments, within industry}}
+ \underbrace{\sum_{s} \Delta \ell_{s}\, \bar y_{s}}_{\text{between industries}}
\;(+\text{ interaction terms})
$$

The middle term is invisible both to sector-level shift-share analysis (which sees only $\ell_s$, $\bar y_s$) and to firm-level datasets that cover only formal firms above a size cut-off.

---

## 2. Five ideas

### Idea 1 — Structural change is about *segments*, not only sectors

**Claim.** In LAC the dominant structural boundary runs between modern and traditional segments *within* industries, not between industries. What looks like "growth-reducing structural change toward services" (McMillan & Rodrik) is largely labor moving from $M$ segments (across manufacturing, mining, utilities, formal services) into $T$ segments (mostly retail, food, personal and transport services, construction). What looks like "industry mix doesn't matter" (IMF 2025) is the same phenomenon seen through formal-firm data, which observes the $M$ segment only.

**Why it matters.** It reconciles tension T1 and redefines the target: the escalator a country needs is *movement from $T$ to $M$*, whatever the industry. A shift into services is not growth-reducing per se; a shift into the $T$ segment of services is.

**Relation to literature.** *Prior art (found 2026-11-02, D-013):* Fentanes & Levy (2024, L101) already show for Mexico, with census data covering formal and informal firms, that the formal–informal composition matters more for TFP than sector composition. Idea 1's remaining contribution is (i) the multi-country version using household surveys, (ii) the explicit reconciliation of McMillan–Rodrik with the IMF industry-mix result, and (iii) the three-way decomposition. Extends Lewis (L002) by placing the traditional sector inside every industry; generalizes the within-manufacturing dualism found by Diao et al. (L051) for Africa; connects structural change to misallocation (L031, L033) by making the segment boundary the main locus of misallocation.

### Idea 2 — The unbundling of the development escalator

**Claim.** An activity's value for development depends on a bundle of five properties:

| Property | Meaning | Indicator (Phase 2) |
|---|---|---|
| **L**evel | productivity premium over the $T$ segment | $y_{sm}/y_T$ |
| **D**ynamism | expected productivity growth / convergence speed | $\hat g_{sm}$; convergence coefficient |
| **A**bsorption | ability to employ many low/mid-skill workers at that productivity | employment elasticity; skill mix; capital per worker |
| **T**radability | demand not bounded by domestic income | export share; tradability index |
| **C**apability building | learning for workers and organizations; spillovers | experience-wage slope; worker flows to entrepreneurship; supplier linkages |

Labor-intensive manufacturing in the second half of the 20th century scored high on all five at once. That is *why* it was the escalator (Kaldor, Rodrik L020, Felipe et al. L067). Today the bundle has come apart:

- Modern manufacturing and mining: high L, D, T; low A (automation, capital intensity — L051, L018's "enclaves").
- Tradable knowledge services (ICT, finance, professional): high L, D, T, C; low A (skill-intensive — L056, L066).
- Labor-absorbing services: high A; low L, D, T, and usually C.

**Implication.** There is no longer a single sector a country can "get into." Development strategy becomes a problem of **rebundling**: combining activities (or upgrading them) so that, in aggregate, the economy raises productivity *and* absorbs labor. This turns Q2 ("what structure is needed?") into a portfolio question rather than a sector-picking question.

**Relation to literature.** Builds on Rodrik's "premature deindustrialization" and services work (L021, L049, L055) and on the services heterogeneity literature (L056), but makes the properties separable and measurable, so that any activity — including resource-based ones — can be scored on the same basis.

### Idea 3 — Jobs as human-capital factories: the dynamic cost of a bad job structure

**Claim.** The most important difference between good and bad jobs, for growth, is how much the job *teaches*. Workers in $M$-segment jobs accumulate human capital (task variety, supervision, exposure to technology and management, internal ladders); workers in $T$-segment jobs accumulate little. Hence:

$$
h_{i,t+1} = h_{i,t}\,\big(1 + \lambda_{m(i,t)}\big), \qquad \lambda_M > \lambda_T ,
$$

and the economy's average human capital growth depends on the share of person-years spent in $M$-type jobs. A structure dominated by $T$ jobs produces flat experience-wage profiles (Lagakos et al. L048), a thin supply of experienced managers, and — because managers and entrepreneurs come out of $M$ jobs — a thin supply of firms able to grow.

**Why it matters.** Static misallocation estimates (F8) understate the cost of LAC's structure. A worker who spends 20 years as a street vendor loses not only the productivity gap each year but the compounding human capital she would have built. This also explains a LAC puzzle: large schooling expansion with disappointing growth — schooling was not complemented by jobs that build on it.

**Prior art (found 2026-11-02, D-013).** Bobba, Flabbi, Levy & Tejada (2021, L102) show for Mexico that human capital upgrades faster in formal than informal jobs; Franco & Quintero (2025, L103) show it for Chile with an endogenous growth model of segmented learning. Idea 3 is therefore established for two countries; the project's contribution would be cross-country evidence and the link to managerial/entrepreneurial supply (P6).

**Testable core.** Experience-wage slopes should be steeper in $M$ than in $T$ jobs *within the same industry and education level*, and workers moving from $T$ to $M$ should see a change in slope, not only in level.

### Idea 4 — LAC's low-productivity equilibrium: interlocking loops

**Claim.** LAC's stagnation is a self-reinforcing equilibrium, not a sum of independent distortions. Four loops sustain it:

1. **Firm–capability loop.** Few firms grow → few $M$ jobs with internal ladders → few workers acquire managerial/organizational capabilities → few capable entrepreneurs and managers → few firms grow. (Ideas 1, 3; L034, L046, L047.)
2. **Social-contract loop.** Social insurance and labor regulation are tied to formal salaried jobs, which are taxed; non-contributory programs and lax enforcement subsidize $T$ (L033). This expands $T$, which shrinks the contributory base, which raises the tax on formal jobs. Politically, a large $T$ population supports non-contributory programs that sustain the arrangement.
3. **Commodity–capability ratchet.** Commodity booms appreciate the real exchange rate and raise demand for non-tradables: labor flows into $T$ services and tradable $M$ activities shrink (L018, L060). In busts, tradable capability destroyed in the boom (firms, supplier networks, workers' skills) is not rebuilt quickly — learning is lost asymmetrically. Repeated cycles ratchet the economy's tradable capability downward. (Testable: asymmetric hysteresis.)
4. **Incumbent–competition loop.** Concentrated markets with high markups (L040) let incumbent large firms earn rents without upgrading; incumbents have political influence over regulation and competition enforcement (L011, L043). Low competitive pressure lowers within-firm productivity growth (F9) and blocks entry of challengers that would create $M$ jobs.

The loops are **complementary**: each raises the payoff of staying in the low state for the actors in the others. This explains (a) why single-dimension reforms (trade liberalization, macro stabilization) under-delivered (Kehoe & Ruhl L063); (b) why LAC missed the post-2000 convergence wave even as its "fundamentals" converged (L044); and (c) how the rival diagnoses in strand 7 can each be partly right.

### Idea 5 — The absorption constraint: why services upgrading needs a tradable engine

**Claim.** In non-tradable activities, productivity growth in the $M$ segment displaces $T$ workers unless demand expands. With segment output $Q_s = y_{sM}L_{sM} + y_{sT}L_{sT}$ facing demand $Q_s = D_s(p_s, Y)$, an upgrade that raises $y_{sM}$ (e.g., supermarkets replacing corner shops) raises aggregate productivity *only* to the extent displaced workers find jobs elsewhere at equal or higher productivity. With low price and income elasticities, the displaced flow into other $T$ activities — productivity rises within the sector but falls elsewhere, the LAC pattern in F5.

Sustained services-led upgrading therefore requires a **tradable engine** that raises national income $Y$ (shifting $D_s$ outward) and/or creates $M$ jobs directly. The engine can be manufacturing, resource-based activities with domestic linkages, or tradable services — but its income must flow broadly into domestic demand (wages, not only rents).

**Implication.** Rodrik–Sandhu's agenda of upgrading labor-absorbing services (L049) is necessary but not sufficient; on its own it can deliver productivity in the upgraded segment and informality elsewhere. Upgrading must be paired with an engine — this is the rebundling logic of Idea 2 at the macro level.

---

## 3. Answers the framework proposes (to be tested)

**Q1 — How do countries grow?** By raising productivity within segments *and* moving people from $T$ to $M$ segments at the same time. The second channel matters most at low and middle income, because it also drives human capital accumulation (Idea 3).

**Q2 — What structure is needed?** Not a particular sector but a portfolio that scores high in aggregate on L, D, A, T and C (Idea 2), with a tradable engine whose income feeds domestic demand (Idea 5).

**Q3 — Are some jobs better?** Yes — measurably, on five dimensions; for growth the decisive ones are capability building and absorption, because they compound and scale. Private and social value diverge through learning and spillovers, so markets under-supply good jobs.

**Q4 — Why does LAC grow slowly?** Because its economy is locked in a low-$M$ equilibrium sustained by four interlocking loops (Idea 4). Its structural change has been from $M$ to $T$ segments (Idea 1); its escalator unbundled before it reached high income (Idea 2); its job structure under-builds human and managerial capital (Idea 3); and its services cannot absorb labor productively without a broad-based tradable engine (Idea 5).

---

## 4. Known weaknesses of v0.1

- The segment boundary ($M$/$T$) is a simplification; formality and size are correlated but distinct. Needs a continuous version.
- Idea 4 is a verbal model; a formal multiple-equilibrium model (e.g., occupational choice with learning and a contributory social-insurance tax) is the next theoretical step (OQ-01).
- Idea 3 must rule out selection: workers who get $M$ jobs may be the fast learners. Needs within-worker variation (OQ-04).
- Resource-based development (Chile copper, Brazil agribusiness) may score better on C than assumed; must be scored, not presumed (OQ-05).
- Caribbean and Central American economies (tourism, remittances, maquila) may not fit the LA5-based facts.
