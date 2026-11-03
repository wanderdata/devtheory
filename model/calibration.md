# Calibration register (trapmodel 0.1.0)

**Status key**
- **illustrative:** chosen so the model reproduces the qualitative facts. Not estimated.
- **anchored:** set to match a documented magnitude (register ID given).
- **to estimate:** a Phase 2 target with a candidate data source.

All values below are baseline unless noted. Scenario-specific values are in `scenarios/*.toml`.

## Targets the baseline is meant to reproduce

| Target | Model object | Evidence | Model v0.1 | Status |
|---|---|---|---:|---|
| ~70% of LAC workers self-employed or in firms < 10 workers | trap-state $u$ | L040 (World Bank 2024); segment definition D-005 | 0.72–0.77 | anchored (loosely) |
| LA5 TFP ≈ 0.52 of US | trap-state $A$ | L041 (IMF 2025) | ≈ 0.51 | anchored (loosely) |
| Escapers' income several times LAC's | GNI escaper / LAC-type | Korea vs. LAC; strand 9 | 2.6× | illustrative |
| Formal-informal productivity gap ~2× or more | $y_M / y_T$ | L033, L088, L101 | to report in v0.2 | to estimate |
| Total payroll-related wedge on formal salaried work | trap-state $\tau$ | Levy (L033) and national tax/contribution schedules | 0.60 (cap) | **too high; to estimate** |

## Parameters

| Section.param | Value | Meaning | Evidence / target | Status |
|---|---:|---|---|---|
| technology.alpha | 0.65 | curvature of firm output (span of control); labor share in modern firms | Lucas (1978)-type models; labor share 0.6–0.7 | illustrative |
| technology.a_T | 0.25 | traditional productivity (units of service) | normalization: sets P ≈ 0.5 | normalization |
| technology.nu | 1.8 | modern-services productivity relative to A | sets when modern services become viable | illustrative |
| technology.psi | 0.40 | tradable share of spending | national accounts / IO tables | to estimate |
| labor.beta | 0.5 (LAC 0.4; escaper 0.7) | value workers place on contributions | Levy (L033); Bobba et al. (L102) | to estimate |
| labor.b | 0.16 (escaper 0.10) | payroll-financed transfer per informal worker, share of non-resource GDP pc | size of non-contributory programs funded by payroll | illustrative; **key lever** |
| labor.u_min | 0.03 | irreducible traditional share | advanced-economy own-account share | illustrative |
| government.g | 0.10 | public goods financed by the payroll wedge, share of non-resource GDP | — | illustrative; **key lever** |
| government.theta_R | 0.5 | state share of retained rents | royalty and resource-tax regimes | to estimate by country |
| government.kappa_R | 0.0 (resource-rich 0.5) | share of state rent used to cut the payroll wedge | procyclical fiscal policy in LAC | illustrative |
| government.tau_max | 0.60 | ceiling on the wedge | — | illustrative; check sensitivity |
| managers.eta_alloc | 4 | sharpness of the tradable/non-tradable choice | — | illustrative |
| managers.eta_part | 4 | sharpness of the decision to run a firm | — | illustrative |
| managers.kappa_m | 2.0 | manager outside option relative to informal income | — | illustrative |
| dynamics.delta_K | 0.04 | capability depreciation (retirement) | ~25-year managerial career | anchored (loosely) |
| dynamics.delta_idle | 0.10 | extra loss for idle managers (ratchet) | — | illustrative |
| dynamics.lam_X / lam_N | 0.020 / 0.008 | managers created per worker-year in tradable / non-tradable modern jobs | P6: founders' prior employment (RAIS, PILA) | to estimate |
| dynamics.k0 | 0.0005 | managers from outside (schooling, FDI) | — | illustrative |
| dynamics.theta_X / theta_N | 0.20 / 0.03 | catch-up per unit of tradable / non-tradable modern employment | Atkin–Costinot–Fukui (L053); experience profiles (L048, L102, L103) | to estimate |
| dynamics.g_star | 0.04 | erosion of relative productivity without catch-up | — | illustrative |
| ownership.rho_F / rho_R | 0 (LAC 0.3 / 0.4) | foreign shares of modern profits / rents | BoP primary income; ECLAC FDI (L099) | to estimate (OQ-17) |
| ownership.sigma_R | 1.0 (resource-rich 0.3) | share of retained rent spent at home | sovereign-fund rules | to estimate |
| commodity.* | scenario-specific | rent path | commodity price indices × resource share of GDP | to estimate |

## Sensitivity checks still to run (v0.2)

1. Does the trap survive with `fiscal_loop=off` if the capability loop gets its own increasing returns? (OQ-22)
2. How does the basin boundary move with `tau_max`, `beta`, `b` and `g`?
3. Are the results robust to `eta_part` and `eta_alloc` (sharp vs. smooth choices)?
