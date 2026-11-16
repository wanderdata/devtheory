# Unbalanced growth, relative prices and the reallocation term

Version 0.1, 2026-11-16. Decisions: D-070, D-071. Propositions: P48–P51. Model code: `apps/productivity/unbalanced.py` (tested in `apps/productivity/tests/test_unbalanced.py`); interactive version: the page *Explainer: unbalanced growth and the decomposition* in the productivity app.

This note puts Baumol's model of unbalanced growth and the McMillan–Rodrik decomposition in one framework, so that the two empirical tools already in this repository, the relative-price slope of WP08 (`09_baumol.py`) and the within/static/dynamic decompositions of WP05, WP06 and WP08, can be read against the same model. It then adds three features of developing economies (an informal wage gap, wages that keep part of their own sector's productivity growth, and markups in protected sectors) and derives what each implies for the two tools. The main results are an exact expression for the relative-price slope in terms of wage and markup pass-through, and the observation that the static reallocation term at current or initial-year prices measures movements across gaps in wages and markups, not across gaps in technology.

## 1. Background

Baumol (1967; L005, L144) considered an economy in which productivity grows in some activities and stagnates in others, and wages are equalised across activities by labour mobility. Unit costs, and with them relative prices, then rise in the stagnant activities in proportion to their productivity gap. If demand for their output is price-inelastic, their share of spending and of employment rises, and aggregate productivity growth falls toward the growth rate of the stagnant activities. Ngai and Pissarides (2007; L173) formalised the mechanism in a multisector growth model: with an elasticity of substitution below one across final goods, employment moves toward sectors with low productivity growth along a path on which aggregate growth is balanced in the limit. Comin, Lashkari and Mestieri (2021; L174) add non-homothetic demand, so that structural change also reflects income effects. Duernecker, Herrendorf and Valentinyi (2022; L175, verified) document that cost disease contributed to the post-war productivity slowdown in the United States and, by distinguishing progressive from stagnant services, find that it is likely to be weaker in future.

McMillan and Rodrik (2011; L018) decompose aggregate labour-productivity growth into growth within sectors and a structural-change term that records the reallocation of labour across sectors with different productivity levels, and find that structural change reduced growth in Latin America after 1990. De Vries, Timmer and de Vries (2015; L118) split the structural term into a static part (reallocation weighted by initial productivity levels) and a dynamic part (reallocation weighted by productivity growth). This repository computes both, at three price bases (D-024, D-032).

The two literatures are rarely connected, although they describe the same objects. Baumol's mechanism is a statement about relative prices and the allocation of labour; the decomposition values labour's reallocation at some set of prices. How the reallocation term behaves in a Baumol economy therefore depends on which prices are used, and on why value added per worker differs across sectors in the first place.

## 2. A three-sector model

There are three sectors. P produces progressive goods (fast productivity growth; manufacturing and tradable services, where innovating firms concentrate). R produces protected services and inputs whose prices carry rents (energy, telecommunications, finance, licensed professions). S produces personal services with slow productivity growth, much of it informal. Labour is the only input:

$$Y_i = A_i L_i, \qquad A_i(t) = e^{g_i t}.$$

Prices are a markup over unit labour cost,

$$p_i = \frac{\mu_i w_i}{A_i},$$

so nominal value added per worker is $p_i A_i = \mu_i w_i$. Value added per worker at current prices differs across sectors only because wages and markups differ.

Wages are $w_i(t) = \rho_i\, e^{\varphi g_i t}$, with $\rho_P = \rho_R = 1$ and $\rho_S = \rho \le 1$ the informal wage relative to the formal wage. The parameter $\varphi \in [0,1)$ is the share of a sector's productivity growth that stays in the sector as higher wages, a reduced form for segmented labour markets, sector-specific bargaining or efficiency wages. Baumol's case is $\rho = 1$, $\varphi = 0$. Markups are $\mu_P = \mu_S = 1$ and $\mu_R(t) = e^{mt}$, so $m > 0$ is a rising markup in the protected sector.

Final demand is CES over the three goods with elasticity of substitution $\varepsilon$ and weights $\omega_i$. Spending shares are

$$s_i = \frac{\omega_i\, p_i^{\,1-\varepsilon}}{\sum_j \omega_j\, p_j^{\,1-\varepsilon}},$$

and, because the wage bill in sector $i$ is $s_i E / \mu_i$, employment shares are

$$\ell_i = \frac{s_i / (\mu_i w_i)}{\sum_j s_j / (\mu_j w_j)}.$$

The model is partial in one respect: wages are set by the rule above rather than by market clearing in a segmented labour market. The informal sector absorbs whatever labour the formal sectors do not employ at their wages, which is the Lewis (1954; L002) reading of $\rho < 1$. A general-equilibrium version would make $\rho$ and $\varphi$ endogenous; the results below hold for any paths of $\rho$, $\varphi$ and $m$ and do not depend on how they are generated.

## 3. Baumol's case

With one wage and no markups, $p_i \propto 1/A_i$ and $\ell_i = s_i$. Differentiating the share equation,

$$\frac{d}{dt}\ln\frac{\ell_i}{\ell_j} = (1-\varepsilon)\,(g_j - g_i).$$

With $\varepsilon < 1$ labour moves toward the sectors with slower productivity growth; with $\varepsilon = 1$ shares are constant; with $\varepsilon > 1$ labour moves toward the fast sectors. Aggregate real productivity growth, measured with a chained index, is to first order $\sum_i \ell_i g_i$: as employment shifts toward slow sectors, aggregate growth falls toward $\min_i g_i$.

In the parameterisation used in the explainer ($g_P = 3\%$, $g_R = 1\%$, $g_S = 0.5\%$, $\varepsilon = 0.5$, initial spending weights 0.40, 0.25 and 0.35), the employment share of S rises from 35% to 46% over 60 years and aggregate growth falls from 1.64% to 1.28% a year. These numbers illustrate the mechanism; they are not calibrated to any country.

## 4. Relative prices and the Baumol slope

Write $\Delta$ for the change in logs over a period, and measure each sector's price and real productivity relative to the economy (the aggregate deflator and aggregate real output per worker). From $p_i = \mu_i w_i / A_i$,

$$\Delta \ln \frac{p_i}{P} = \Delta \ln \mu_i + \Delta \ln w_i - \Delta \ln A_i - c,$$

where $c$ is common to all sectors. Step 09 of the labour-productivity pipeline regresses the left-hand side on $\Delta \ln (A_i / \bar A)$ across sectors and countries. The slope of that regression is

$$b = -1 + \frac{\operatorname{cov}(\Delta \ln w_i, \Delta \ln A_i) + \operatorname{cov}(\Delta \ln \mu_i, \Delta \ln A_i)}{\operatorname{var}(\Delta \ln A_i)}.$$

In Baumol's case both covariances are zero and $b = -1$. With the wage rule of section 2 and constant markups, $b = -(1 - \varphi)$ exactly. A rising markup in a slow sector makes the second covariance negative and pushes $b$ below $-1$; a rising markup in a fast sector pushes it toward zero.

The estimated slope for Latin America and the Caribbean, pooled over 27 countries and five sectors (mining and utilities excluded), is −0.48 for 2000–2019, with a 90% bootstrap interval over countries of −0.62 to −0.29 (`empirics/output/lac_lp/baumol/slope.csv`); for the Caribbean (11 countries) it is −0.40 (−0.62 to −0.14). Read through the expression above, these estimates mean that relative prices offset about half of the differences in real productivity growth across sectors, and that the other half shows up as differences in nominal value added per worker, which in this model are differences in wages and markups. A pass-through of $\varphi \approx 0.5$ is one way to produce this. Two caveats limit that reading. First, measurement error in sector employment moves real and nominal productivity together and biases the estimate toward zero, while errors in sector deflators bias it toward −1 (OQ-59); the slope re-estimated between survey years with survey employment is −0.30 (−0.52 to −0.10), so attenuation is not obviously the explanation, but it cannot be ruled out. Second, a slope above −1 can also come from rising markups in fast-growing sectors, which the wage interpretation does not distinguish. The two can be separated with data on compensation and operating surplus by sector (P48).

## 5. What the decomposition measures

### 5.1 The terms in the model

For a step from $t$ to $t+1$, let $y_i$ be value added per worker valued at some fixed prices $\bar p_i$, so $y_i = \bar p_i A_i$. The decomposition used in this repository is

$$\Delta Y = \underbrace{\sum_i \ell_{i,t}\,\Delta y_i}_{\text{within}} + \underbrace{\sum_i y_{i,t}\,\Delta \ell_i}_{\text{static}} + \underbrace{\sum_i \Delta y_i\,\Delta \ell_i}_{\text{dynamic}}.$$

At initial-year prices, $\bar p_i = p_{i,t}$ and $y_{i,t} = \mu_{i,t} w_{i,t}$. The static term is therefore

$$\text{static} = \sum_i \mu_{i,t}\, w_{i,t}\, \Delta \ell_i,$$

a weighted sum of employment changes with weights equal to wages times markups. It records movements of labour across gaps in wages and markups. Gaps in technology enter only through their effect on wages and markups.

### 5.2 Baumol's case

With one wage and no markups, every sector has the same nominal value added per worker, and the static term at initial-year prices is exactly zero, however much labour moves. The slowdown appears in two other places: in the within term, because the employment weights on fast sectors shrink, and in the dynamic term, which is $\sum_i \bar p_i A_{i,t}(e^{g_i} - 1)\Delta \ell_i$ and is negative because employment grows where $g_i$ is low. The dynamic term is second order for one year, but over a period of $h$ years both $\Delta y_i$ and $\Delta \ell_i$ grow roughly in proportion to $h$, so in long-period decompositions it grows with the square of the period's length. This is one reading of the "dynamic losses" that de Vries, Timmer and de Vries (2015) find in Africa.

At the prices of a distant base year, $y_{i,t} = p_{i,0} A_{i,t}$ grows faster in fast sectors, and the static term becomes negative even in Baumol's case: labour leaves sectors whose base-year-price productivity has risen. In the explainer's Baumol parameterisation the static term averages −0.19 percentage points a year over 60 years at year-0 prices and exactly zero at chained prices, for the same economy. Whether a decomposition reports structural change as growth-reducing can therefore depend on the price base alone, which is the reason D-024 values each period at its own initial-year prices and D-032 reports three bases.

### 5.3 Wage gaps and markups

With an informal wage gap, the static term at initial-year prices is

$$\text{static} = w\,(\Delta \ell_P + \Delta \ell_R) + \rho\, w\, \Delta \ell_S + (\mu_R - 1)\, w\, \Delta \ell_R = -(1-\rho)\, w\, \Delta \ell_S + (\mu_R - 1)\, w\, \Delta \ell_R,$$

using $\sum_i \Delta \ell_i = 0$ and setting $\varphi = 0$ for clarity. Growth-reducing structural change in this term means that employment moved into the low-wage sector; it is negative whenever informal employment grows, whatever the reason. In the explainer's dual-economy parameterisation ($\rho = 0.45$, $\varphi = 0.5$) the static term averages −0.35 points a year at chained prices.

The second term has the opposite sign from the first and a different interpretation. A movement of labour into a sector with a high markup raises the static term, although nothing about technology has changed: the term counts rents as productivity. McMillan and Rodrik's finding that structural change reduced growth in Latin America after 1990 is consistent with movements into informal work at lower wages; a positive static term in a period when employment grew in protected, high-margin services would need to be checked against those sectors' operating surplus before being read as productive reallocation (P50).

## 6. Three features of developing economies

The three parameters added to Baumol's model correspond to features documented elsewhere in this project.

The informal wage gap $\rho$ makes informal personal services cheap. With $\varepsilon < 1$, a lower relative price of S lowers S's spending share, but each unit of spending on S employs more workers, and for the parameter values used here the second effect dominates: the initial employment share of S is 44.5% with $\rho = 0.45$ against 35% with $\rho = 1$. The same informal wage gap appears in the earnings data of WP09 (studies 9.2 and 9.3).

Wage pass-through $\varphi$ lets workers in fast sectors keep part of their productivity growth as higher wages. Prices of fast-growing goods then fall by less, labour leaves the fast sector faster, and the relative-price slope rises from −1 toward zero. In the explainer, $\varphi = 0.5$ reproduces a slope of −0.50, close to the regional estimate.

A rising markup $m$ in the protected sector raises R's relative price beyond its productivity gap. With $\varepsilon < 1$, R's spending share rises, but because part of that spending is profit, R's employment share can fall, and the labour released goes to S. In the explainer, $m = 1\%$ a year added to the dual economy raises S's employment share after 60 years from 61% to 65% and lowers aggregate growth in year 60 from 1.15% to 1.04%. Markups enter the input costs of other sectors when R supplies intermediate inputs (Jones 2011; L176), which this labour-only model omits; that channel would add to the slowdown.

The demand weights $\omega_i$ can stand in for income distribution. With non-homothetic preferences, a high top-income share raises the weight on labour-intensive personal services, which holds labour in S (Comin, Lashkari and Mestieri 2021). The explainer lets the user change the weights directly.

Together with Baumol (1990; L177), on the allocation of entrepreneurship between productive and unproductive activities, these features describe a loop. The markup that raises R's spending share also raises the return to capturing a protected position, so the same barriers that shift spending toward R shift entrepreneurs toward it. This connects the note to the establishment-level classification of innovating, rent-dependent and replicative businesses planned for Mexico with DENUE (D-071), and to Parente and Prescott (1999; L178) on monopoly rights as a barrier to technology adoption.

## 7. Propositions

| # | Proposition | Source | Support if… | Reject if… | Data |
|---|---|---|---|---|---|
| P48 | Across sectors, the part of relative real productivity growth not offset by relative prices (slope above −1 in 09_baumol) is mainly relative wage growth, not relative markup growth. | §4 | in a regression of each sector's relative change in compensation per worker on its relative real productivity change, the coefficient is positive and at least half of (1 + b) | coefficient near zero while operating surplus per worker carries the difference | UN AMA compensation and gross operating surplus where available; Mexico: Economic Censuses 2004–2024 (remunerations, gross value added), INEGI KLEMS |
| P49 | Differences in value added per worker at current prices across sectors are mostly differences in average labour compensation and operating surplus per worker that track formality, not differences in technology measured at a common price. | §5.1 | in Mexico, the cross-sector variance of current-price value added per worker is explained mostly by compensation per worker and the formal share, conditional on sector | the variance is mostly within the operating surplus of high-markup sectors, or unrelated to formality | Economic Censuses; ENOE (9.3); MEITEF |
| P50 | Positive static reallocation terms at initial-year prices partly reflect employment growth in high-margin protected services. | §5.3 | in country-periods with a positive static term, the sectors that gained employment had operating surplus per worker above the economy-wide average by more than their compensation gap | gains came from sectors whose compensation per worker exceeds the average with ordinary margins | UN AMA (compensation and surplus), Mexico Economic Censuses |
| P51 | In Mexico, relative prices of rent-prone sectors rose more than their relative productivity growth predicts. | §4, §6 | residuals of the slope regression (INEGI KLEMS, 1990–2023) are positive on average for sectors classified as rent-prone ex ante (utilities, telecommunications before 2013, finance, fuel retail before 2016), with an interval excluding zero | residuals of rent-prone sectors no different from others | INEGI KLEMS; INPC; reform dates |

## 8. Limitations

The model has no capital, no intermediate inputs and no trade. Trade matters most: Baumol's mechanism applies to non-tradables, whose demand is domestic, while a tradable sector faces world demand and can grow without its relative price falling at home (see `docs/literature/03_industrialization_and_services.md`). Wages follow a rule rather than clearing a labour market, so the model describes how given wage gaps and markups show up in prices and decompositions; it does not explain them. The results of sections 4 and 5 are accounting results that hold for any paths of wages, markups and productivity, which is what makes them useful for reading the estimates, but they identify nothing causal by themselves.

## References

Register IDs in parentheses; L173–L178 added with this note.

- Baumol, W. J. (1967). Macroeconomics of unbalanced growth: the anatomy of urban crisis. *American Economic Review* 57(3): 415–426. (L005, L144)
- Baumol, W. J. (1990). Entrepreneurship: productive, unproductive, and destructive. *Journal of Political Economy* 98(5): 893–921. (L177)
- Comin, D., Lashkari, D. and Mestieri, M. (2021). Structural change with long-run income and price effects. *Econometrica* 89(1): 311–374. (L174)
- de Vries, G., Timmer, M. and de Vries, K. (2015). Structural transformation in Africa: static gains, dynamic losses. *Journal of Development Studies* 51(6). (L118)
- Duernecker, G., Herrendorf, B. and Valentinyi, Á. (2022). Structural change within the services sector and the future of cost disease. Working paper. (L175)
- Jones, C. I. (2011). Intermediate goods and weak links in the theory of economic development. *American Economic Journal: Macroeconomics* 3(2): 1–28. (L176)
- Lewis, W. A. (1954). Economic development with unlimited supplies of labour. *The Manchester School* 22(2). (L002)
- McMillan, M. and Rodrik, D. (2011). Globalization, structural change and productivity growth. NBER Working Paper 17143. (L018)
- Ngai, L. R. and Pissarides, C. A. (2007). Structural change in a multisector model of growth. *American Economic Review* 97(1): 429–443. (L173)
- Parente, S. L. and Prescott, E. C. (1999). Monopoly rights: a barrier to riches. *American Economic Review* 89(5): 1216–1233. (L178)
