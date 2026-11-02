# Which Firms Are Good for Growth? Three Ledgers for Judging a Firm's Contribution to Development

**devtheory Working Paper 01** · Draft v0.1 · 2 November 2026
Project: Productive Development in Latin America and the Caribbean ([repository README](../../README.md))

---

## Abstract

Policy debates about "good firms" mix up three different questions: how much a firm adds to GDP, how much of that income stays in the country and circulates, and whether the firm makes the economy more productive over time. This paper separates them into three ledgers. The **production ledger** counts value added, not sales; imports are subtracted in the GDP identity only to cancel imported content already counted elsewhere, so they never reduce GDP mechanically, and a firm's real contribution is its value added *net of what its workers and capital would otherwise have produced*. The **income-and-demand ledger** follows the money: profits remitted abroad leave GDP but not GNI, workers' spending circulates domestically only to the extent that it is not spent on imports, and in a balance-of-payments-constrained economy the net foreign exchange a firm earns sets a ceiling on everyone else's growth. The **capability ledger** asks whether the firm raises productivity in itself, its suppliers and its workers. Worked examples with seven stylized firm types (a foreign copper mine, a maquila assembler, an agro-exporter, a software exporter, a hotel, a supermarket chain and informal corner shops), all with the same US$100m of sales, show that rankings flip from one ledger to the next. The firms that are good for growth in Latin America are those that score on all three at once: tradable, embedded in domestic supply chains, nationally retained income, labor-absorbing at above-informal productivity, and learning-intensive. Few firms do; that scarcity is a large part of the region's growth problem.

---

## 1. The question, and why it needs three ledgers

Ask a finance ministry which firms are good for growth and you get *exporters*. Ask a labor ministry and you get *employers*. Ask a central bank and you get *firms that earn dollars*. Ask an economist and you get *productive firms*. All four are partly right, because they are answering different questions:

| Ledger | Question | Time horizon | Core concept |
|---|---|---|---|
| A. Production | How much does the firm add to GDP? | Now | Value added, net of opportunity cost |
| B. Income and demand | Who receives that value added, where do they spend it, and what does it do to the external accounts? | Short to medium run; long run if balance-of-payments constrained | GNI, multiplier, net foreign exchange |
| C. Capability | Does the firm make the economy more productive over time? | Long run | Productivity growth, learning, linkages |

A firm can score high on one ledger and low on the others. A copper mine has enormous value added per worker (ledger A), sends much of it abroad and spends little locally (ledger B), and may or may not build domestic capabilities (ledger C). Most confusion in public debate comes from reading one ledger and drawing a conclusion that only the others could support.

---

## 2. Ledger A — production: value added, not sales

### 2.1 The identity and the "imports reduce GDP" mistake

The expenditure identity is

$$
Y = C + I + G + X - M .
$$

It is tempting to read the minus sign as "imports reduce GDP." They do not. $C$, $I$, $G$ and $X$ are measured at purchasers' prices and *include* imported content: the imported phone in a household's consumption, the imported machine in investment, the imported chips inside an exported car. $M$ is subtracted only to remove that content, so that $Y$ counts domestic production once. If a household switches from a domestic phone to an imported one, $C$ is unchanged, $M$ rises, and GDP falls by the domestic value added of the phone it no longer buys — not because of the import, but because domestic production fell. If instead the import is a component that lets a domestic firm export, $X$ rises by the full sale and $M$ by the component, and GDP rises by exactly the domestic value added.

This is the "both sides of the ledger" point: part of every sale appears in $X$ (or $C$, $I$, $G$) and again in $M$, and the two cancel. What remains is the **production identity**

$$
Y = \sum_{\text{firms}} VA_j, \qquad VA_j = \text{Sales}_j - \text{Intermediate inputs}_j = W_j + \Pi_j + T_j ,
$$

where $W$ is wages, $\Pi$ gross operating surplus (profits, rents, depreciation) and $T$ net taxes on production. A firm's GDP contribution is its value added, and value added is just the income it generates for workers, owners and the state.

### 2.2 Direct versus supply-chain value added

A firm also creates value added in its domestic suppliers, who in turn import part of their inputs. Total domestic value added generated per dollar of the firm's sales is

$$
\text{DVA}_j = \text{Sales}_j - M^{\text{direct}}_j - M^{\text{indirect}}_j ,
$$

or, with an input–output matrix of domestic input coefficients $A^d$ and value-added coefficients $v$, $\text{DVA} = v'(I - A^d)^{-1}$ per unit of final output. The difference between the two can be large. Mexico's maquila export plants are the textbook case: the domestic value added share of maquila exports fell from about 31% in 1981 to about 21% in 2006 (Castillo & de Vries). A dollar of maquila exports adds about twenty cents to Mexican GDP; a dollar of agricultural exports, with mostly domestic inputs, adds much more. **Gross exports are a poor measure of a firm's contribution; domestic value added in exports is the right one.**

### 2.3 Opportunity cost: the step almost everyone skips

Value added is a gross contribution. The firm's workers and capital would have produced *something* elsewhere. The firm's net contribution to GDP is

$$
\Delta Y_j = VA_j - \sum_{k \in \text{inputs of } j} \text{(what input } k \text{ would otherwise produce)} \;\approx\; VA_j - L_j\, y^{\text{alt}} - r\,K_j ,
$$

where $y^{\text{alt}}$ is value added per worker in the workers' next-best activity and $rK_j$ is the return capital would earn elsewhere.

This is where development economics enters. In a fully employed economy where labor is paid its marginal product everywhere, $y^{\text{alt}}$ is close to the firm's own wage, and a new firm adds little *net* GDP — it mostly moves resources around. In a **dual economy**, where most workers' alternative is low-productivity informal self-employment (Lewis 1954; strand 2 of this project), $y^{\text{alt}}$ is far below what a modern firm pays and produces. Each job in a modern firm then adds the *gap* between modern and informal productivity. In Latin America, where about 70% of workers are self-employed or in firms with fewer than ten workers (World Bank 2024), this gap — not the firm's gross value added — is the right measure of a job's contribution to output.

Two implications are worth stating sharply:

- **"More jobs means more GDP" is only true net of where the workers came from.** A firm that hires informal vendors at higher productivity raises GDP; a firm that hires workers away from another formal firm at equal productivity does not.
- **A firm that raises productivity by shedding labor raises GDP only if the shed workers find work at least as productive as before.** If they fall back into informality, part of the firm's gain is offset elsewhere. This is the core of the absorption problem discussed in Section 5.

---

## 3. Ledger B — income and demand: where the money goes

### 3.1 GDP versus national income: whose value added is it?

Value added is produced in the country, but it is not necessarily *income of the country*. Profits of foreign-owned firms, interest on foreign debt and royalties paid abroad are part of GDP but not of gross national income (GNI):

$$
\text{GNI} = \text{GDP} + \text{primary income received from abroad} - \text{primary income paid abroad}.
$$

**Ireland** is the extreme example. Irish GDP grew 26% in 2015, mostly because multinationals relocated intellectual property into Irish affiliates; by 2019 the Central Bank of Ireland's preferred domestic measure, GNI\*, was about 40% below GDP. Ireland ranks first in Europe (ex-Luxembourg) on GDP per head but around 12th on consumption per head (Central Bank of Ireland 2021). A firm that books profits in a country raises its GDP without necessarily raising anyone's income there.

The Latin American version is quieter but persistent. Chile runs a goods trade surplus driven by copper, yet its current account was in deficit (1.5% of GDP in 2024), with deficits on services and primary income — the latter including profits paid to foreign owners of mines and other investments (Banco Central de Chile data as reported by Diario Estrategia). For a foreign-owned mine, what stays in the country is wages, payments to domestic suppliers, taxes and royalties. **The fiscal regime is therefore not a side issue in judging extractive firms; it determines most of their national-income contribution.**

### 3.2 Distribution and the demand multiplier

Value added becomes wages and profits, and the two are spent differently. Workers spend most of their income; owners save more of theirs. Each round of spending leaks out of the domestic circular flow through saving, taxes and imports. The standard open-economy multiplier is

$$
k = \frac{1}{1 - c(1-t) + m},
$$

where $c$ is the marginal propensity to consume, $t$ the tax rate and $m$ the marginal propensity to import. What matters for a particular firm is the composition of its value added and the spending patterns of those who receive it:

- **Wage-intensive firms** inject more first-round consumption than profit-intensive ones.
- **Workers whose consumption basket is mostly domestic** — food, housing, local services, transport — generate more domestic demand per dollar than high earners whose marginal spending goes to imported cars, electronics and travel.
- **Remitted profits** generate no domestic demand at all.

This is the theoretical core of the intuition that some jobs "increase consumption without an equal and opposite increase in imports." It is correct, with a refinement: no job's income avoids imports entirely; the question is the *import propensity of the marginal spending it finances*. A low-wage worker in Santiago spends more of each extra peso on domestically produced goods and services than a high-wage engineer, but the engineer has many more pesos.

There is also good evidence that tradable jobs pull non-tradable jobs behind them. In US cities, each additional manufacturing job is associated with about 1.6 additional local non-tradable jobs; for skilled jobs the figure is about 2.5, and for high-tech jobs about 4.9 (Moretti 2010). The mechanism is exactly this ledger: tradable firms bring outside income into the locality, and their workers spend part of it on local services.

**Distribution cuts both ways.** Higher wages raise consumption demand; higher profits finance investment. Bhaduri & Marglin (1990) show that whether an economy's demand is *wage-led* or *profit-led* depends on which effect dominates. Studies generally find large advanced economies wage-led and more open developing economies (including Mexico) profit-led once trade is taken into account. East Asia's high-growth phase rested on high profit shares that were *reinvested domestically* (the Lewis–Kaldor mechanism). The developmental question is therefore not "wages or profits?" but **"are the profits reinvested at home, and are the wages spent at home?"**

### 3.3 Why demand matters in the long run: the external constraint

In standard growth theory, demand matters only in the short run; in the long run output is set by supply. Latin America's history suggests a qualification. Growth episodes repeatedly ended in balance-of-payments crises: rising income pulls in imports faster than exports grow, the current account deficit widens, capital flows reverse, and growth stops. Thirlwall's law (1979) formalizes this:

$$
y_{BP} = \frac{x}{\pi},
$$

where $y_{BP}$ is the growth rate consistent with a sustainable external balance, $x$ the growth rate of exports and $\pi$ the income elasticity of demand for imports. In such an economy, **the binding constraint on everyone's growth is foreign exchange**, and a firm's contribution includes how much it loosens that constraint.

A firm's **net foreign exchange contribution** is

$$
\text{NFX}_j = X_j - M^{\text{direct}}_j - M^{\text{indirect}}_j - \text{remitted profits}_j - \text{royalties and fees abroad}_j .
$$

For a firm that exports all its output, NFX equals its contribution to national income (domestic value added minus remitted income). For a firm that sells only at home, NFX is the negative of the import content of what it supplies. Note what this does to the "import substitution" intuition: a domestic firm that replaces imports raises NFX only to the extent that its own import content and remittances are below those of the imports it replaces. A car assembled at home from imported kits saves little foreign exchange.

Two ways to raise the external ceiling follow from Thirlwall's law: raise $x$ (export more, and export goods whose world demand grows fast), or lower $\pi$ (supply domestically more of what rising incomes demand). The second route has a bad history in the region: import-substituting industrialization lowered $\pi$ behind high tariffs, at the cost of high-cost producers and low productivity growth. A *good* low $\pi$ comes from competitive domestic supply, not from protection.

---

## 4. Ledger C — capability: does the firm make the economy more productive?

Ledgers A and B describe a firm at a point in time. Long-run growth is productivity growth, so the decisive question is dynamic. A firm raises aggregate productivity through five channels:

1. **Its own productivity growth.** Tradable firms face world competition and world technology; unconditional convergence is a property of formal manufacturing (Rodrik 2013).
2. **Reallocation.** It absorbs workers from lower-productivity activities (the opportunity-cost gap of Section 2.3, repeated every year).
3. **Supplier upgrading.** Multinationals raise the productivity of domestic *suppliers* through backward linkages, not of domestic competitors: in Lithuania, a one-standard-deviation increase in foreign presence among downstream customers was associated with about 15% higher output for each supplying domestic firm, with the effect coming from partially rather than wholly foreign-owned projects, which sourced more locally (Javorcik 2004).
4. **Worker learning.** Experience-wage profiles are about twice as steep in rich as in poor countries (Lagakos et al. 2018). Firms with internal hierarchies, training and exposure to technology build human capital; informal micro-units build little.
5. **Diffusion through people.** Managers and workers who leave productive firms carry practices into new firms and suppliers, and are disproportionately the founders of new growing firms (a proposition, P6, this project will test).

---

## 5. Seven firms, three ledgers: worked examples

Table 1 applies the three ledgers to seven stylized firms with identical sales of US$100m. Parameters are **illustrative orders of magnitude**, not estimates for specific firms — except the maquila domestic value-added share, calibrated to the ~21% cited above. All numbers are produced by [`ledger_examples.py`](ledger_examples.py), where every assumption is listed and can be changed. Key assumptions: domestic suppliers' output contains 25% imported content; informal value added per worker (the opportunity cost of labor) is US$5,000; consumption propensities are 0.9 out of wages and 0.3 out of domestically retained profits; the import share of consumption is 20% for low-wage earners, 40% for high-wage earners and 45% for owners.

**Table 1. Seven firms with US$100m of sales (US$ millions unless stated)**

| Firm | Direct VA | Domestic VA (incl. suppliers) | National income retained | Net FX | 1st-round domestic demand | Workers | VA per worker (US$) | Net VA gain vs. informal |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Foreign copper mine | 60 | 78.8 | 41.8 | 41.8 | 4.3 | 80 | 750,000 | 59.6 |
| Maquila electronics assembly | 17 | 23.0 | 18.0 | 18.0 | 7.2 | 1,000 | 17,000 | 12.0 |
| Domestic fruit agro-exporter | 60 | 82.5 | 82.5 | 72.5 | 25.7 | 3,000 | 20,000 | 45.0 |
| Domestic software/BPO exporter | 75 | 86.2 | 86.2 | 86.2 | 32.2 | 1,100 | 68,182 | 69.5 |
| Domestic hotel (foreign guests) | 55 | 77.5 | 77.5 | 77.5 | 24.9 | 1,500 | 36,667 | 47.5 |
| Modern supermarket chain | 16 | 52.8 | 52.8 | −47.2 | 7.3 | 900 | 17,778 | 11.5 |
| Informal corner shops | 15 | 56.2 | 56.2 | −43.8 | 10.8 | 3,000 | 5,000 | 0.0 |

*For the two retailers, "domestic VA incl. suppliers" includes the domestic value added embodied in the goods they sell, and net FX is the import content of those goods.*

What the table shows:

**The copper mine wins Ledger A and loses Ledger B.** It has the highest value added per worker by an order of magnitude, but almost half of its domestic value added leaves as profits and fees, and its local demand injection is the smallest in the table. What the country keeps is the 17 in taxes and royalties, the 8 in wages, and the value added of its domestic suppliers. Raise the remittance share or cut the royalty and the mine's national-income contribution falls one-for-one. Its Ledger C score depends entirely on whether it builds a domestic supplier base (Chile's mining-supplier programs are the relevant experiment).

**The maquila looks large in trade statistics and small in national income.** US$100m of exports become US$23m of domestic value added and US$18m of net foreign exchange. Its real contribution is jobs: 1,000 workers at more than three times informal productivity, with wages spent mostly at home. Its Ledger C score depends on whether it moves up from assembly — the decline in maquila domestic value added since 1981 suggests that, on average, it did not.

**The domestic agro-exporter, software exporter and hotel score well on all of Ledger B.** They are domestically owned, use mostly domestic inputs, export, and pay wages that are spent at home. The agro-exporter is the strongest *absorber* (3,000 jobs at four times informal productivity); the software exporter has the highest net FX and local demand but needs skilled workers, so it absorbs few of the informal workforce; the hotel sits between them. These three are much closer to the "good firm" profile than either the mine or the maquila, even though the mine's value added per worker is more than ten times theirs.

**The supermarket–corner shop comparison is the most counter-intuitive.** Replacing US$100m of corner-shop sales with a supermarket chain raises value added per worker from US$5,000 to about US$17,800 and frees 2,100 workers. If those workers find jobs at the informal average, the economy gains only the supermarket's net gain of about US$11.5m. Meanwhile the chain imports a larger share of what it sells (net FX worsens by about US$3.4m), and local first-round demand falls because 2,100 people lose their income. **Productivity in retail rises; aggregate productivity rises much less; the external balance worsens.** This is the absorption constraint (framework Idea 5): upgrading non-tradable services raises aggregate productivity only if displaced workers move into better jobs, which requires a tradable engine creating them.

**No firm wins everything.** The firm types that score highest on value added per worker (mine, software) absorb few workers; the ones that absorb most (agro-exports, corner shops) have low productivity; the high-volume exporter with many jobs (maquila) retains little value. This is the unbundling of the development escalator (framework Idea 2), seen at the level of a single firm.

---

## 6. So which firms are good for growth?

Putting the ledgers together, a firm is good for a developing economy's growth to the extent that it:

1. **Creates value added well above its workers' alternative** (Ledger A, net of opportunity cost) — the productivity gap times the number of workers it absorbs.
2. **Retains income nationally** — domestic ownership, or foreign ownership with a fiscal regime that captures rents (Ledger B).
3. **Earns or saves foreign exchange net of its own import content and remittances** (Ledger B, external constraint).
4. **Pays income that is spent domestically and reinvests profits at home** (Ledger B, demand).
5. **Raises productivity over time** in itself, its suppliers and its workers (Ledger C).

Ranked by what usually binds in Latin America:

- When the economy is **balance-of-payments constrained** (most of the region's history), net foreign exchange (3) is the gatekeeper: without it, gains on the other criteria are cut short by external crises.
- With **large informal labor surpluses**, absorption at above-informal productivity (1) gives the largest static gains.
- Over **decades**, capability (5) is what compounds; criteria 1–4 decide whether a growth episode lasts long enough for it to matter.

The best firms score on all five at once. In the region these are typically **domestically embedded tradable firms**: agro-industrial exporters with domestic processing and suppliers; tourism with local sourcing and ownership; tradable services; manufacturing that has moved beyond pure assembly; and resource firms that have built domestic supplier and knowledge industries around them. The region's problem is that it has too few of them, and that each of its large firm types is strong on one ledger and weak on the others.

---

## 7. Six common errors, corrected

1. **"Imports reduce GDP."** They don't; the subtraction in $Y = C + I + G + X - M$ only removes imported content counted elsewhere. Imports matter through the external constraint and through displacement of domestic production, not through accounting.
2. **"Exports are growth."** Only their domestic value added is. A dollar of maquila exports added about twenty cents to Mexican GDP by 2006.
3. **"Jobs are GDP."** Only the gap between a job's productivity and the worker's alternative is.
4. **"GDP is national income."** Not when profits leave: Ireland's GDP overstates national income by around 40%; for Latin American extractive sectors, taxes and royalties decide how much of the value added the country keeps.
5. **"Consumption drives growth."** In the short run, or when there is slack. In the long run consumption-led growth hits the external constraint unless exports grow in step.
6. **"Higher wages are always better for growth" (or "higher profits are").** Wages support demand; profits finance investment. What matters is whether the wages are spent and the profits reinvested at home.

---

## 8. Implications for this project

This paper adds two properties to the five-property framework of `docs/theory/01_framework.md` (Level, Dynamism, Absorption, Tradability, Capability): **income Retention** (the share of value added that remains national income) and **net Foreign exchange** (NFX). These matter most for resource-based and foreign-owned firms, which the original framework did not distinguish from domestic ones (decision D-009). It also suggests two empirical exercises for Phase 2:

- **E1.** For the largest LAC economies, compute DVA, retained national income and NFX per dollar of sales by industry and ownership, using OECD TiVA, national input–output tables and balance-of-payments primary income data.
- **E2.** Estimate local multipliers (à la Moretti) for LAC regions by type of tradable activity — mining, maquila, agro-export, tourism — to test whether domestically embedded tradables generate more non-tradable formal employment than enclaves.

---

## References

- Bhaduri, A. & Marglin, S. (1990). Unemployment and the real wage: the economic basis for contesting political ideologies. *Cambridge Journal of Economics*, 14(4), 375–393.
- Castillo, J. C. & de Vries, G. Maquiladoras and domestic value added in Mexico's exports. Paper presented at the 22nd International Input–Output Conference (IIOA). [Link](https://www.iioa.org/conferences/22nd/papers/files/1445_20140312110_MAQfinal.pdf)
- Central Bank of Ireland (2021). Is Ireland really the most prosperous country in Europe? *Economic Letter* Vol. 2021, No. 1. [Link](https://www.centralbank.ie/docs/default-source/publications/economic-letters/vol-2021-no-1-is-ireland-really-the-most-prosperous-country-in-europe.pdf)
- Diario Estrategia (2025). Cuenta corriente de Chile registró déficit de 1,5% del PIB en 2024 (Banco Central de Chile data). [Link](https://www.diarioestrategia.cl/texto-diario/mostrar/5220964/cuenta-corriente-chile-registro-deficit-15-pib-2024)
- Javorcik, B. S. (2004). Does foreign direct investment increase the productivity of domestic firms? In search of spillovers through backward linkages. *American Economic Review*, 94(3), 605–627.
- Lagakos, D., Moll, B., Porzio, T., Qian, N. & Schoellman, T. (2018). Life cycle wage growth across countries. *Journal of Political Economy*, 126(2).
- Lewis, W. A. (1954). Economic development with unlimited supplies of labour. *Manchester School*, 22(2).
- Moretti, E. (2010). Local multipliers. *American Economic Review: Papers & Proceedings*, 100(2), 1–7.
- Rodrik, D. (2013). Unconditional convergence in manufacturing. *Quarterly Journal of Economics*, 128(1).
- Thirlwall, A. P. (1979). The balance of payments constraint as an explanation of international growth rate differences. *Banca Nazionale del Lavoro Quarterly Review*, 128(1), 45–53.
- World Bank (2024). *Competition: The Missing Ingredient for Growth?* Latin America and the Caribbean Economic Review, April.
