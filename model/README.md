# trapmodel — a tunable model of the middle-income "segment trap"

Code for **[WP04](../papers/WP04_trap_model/WP04_segment_trap_model.md)**. Current version: **0.1.1** (see [CHANGELOG](CHANGELOG.md)).

The model is deliberately small. It is meant to be tuned, extended and confronted with data. It is not meant to forecast.

## Files

| File | What it is |
|---|---|
| `trapmodel.py` | The model: parameters (`DEFAULTS`), static equilibrium (`solve_static`), dynamics (`step`, `simulate`, `steady_state`) |
| `scenarios/*.toml` | Scenarios. Each one lists only what differs from `baseline.toml` (via `inherit`) |
| `run.py` | Runs one scenario and writes `output/<scenario>/paths.csv` and `paths.png` |
| `experiments.py` | Regenerates the WP04 experiment figures and tables (E1–E5) |
| `visuals.py` | Regenerates the four summary figures (V1–V4: landscape, fiscal crossing curves, attribution, ratchet) |
| `explorer_data.py` | Precomputes results on a grid of settings for the interactive explorer |
| `explorer/index.html` | The interactive Segment Trap Explorer (reads `explorer/explorer_data.json`) |
| `tests/test_trapmodel.py` | Accounting identities and the key qualitative results |
| `calibration.md` | Every parameter: meaning, current value, target or evidence, status |

## Quick start

```bash
pip install numpy scipy matplotlib pytest      # Python ≥ 3.11 (uses tomllib)
python model/run.py model/scenarios/lac_type.toml
python model/run.py model/scenarios/lac_type.toml --set labor.b=0.08 --tag smaller_transfers
python model/run.py model/scenarios/lac_type.toml --switch fiscal_loop=off --tag no_fiscal_loop
python model/experiments.py                    # WP04 experiment figures/tables (a few minutes)
python model/visuals.py                        # four summary figures (~10 minutes; --reuse skips the ridge)
python model/explorer_data.py                  # explorer data (~25 minutes)
cd model/explorer && python -m http.server     # then open http://localhost:8000
python -m pytest model/tests -q                # must pass before any commit
```

## How to tune

1. **Change a parameter for one run:** `--set section.param=value`.
2. **Switch a mechanism off:** `--switch name=off`. The mechanisms are `capability_loop`, `learning_loop`, `fiscal_loop`, `rent_absorption`, `ratchet` and `remittances`.
3. **Make a new scenario:** copy a `.toml` and keep `inherit = "baseline.toml"`. List only what differs.
4. **Time-limited policies:** add `[[events]]` blocks with `start`, `end`, `section`, `param` and `value`. See `escaper.toml`.
5. **Change the structure:** edit `trapmodel.py`. Then bump `MODEL_VERSION`, add a CHANGELOG entry, rerun the tests and `experiments.py`, and log the decision in `docs/register/decision_log.md`.

**Rule:** any number quoted in a paper must come from `experiments.py` output (`papers/WP04_trap_model/results.md` or `tables/`), not from an ad hoc run.

## The model in one page

A small open economy with a labor force of 1. All values are in units of the tradable good, whose world price is 1. Non-tradable services have price $P$.

**Segments.** Workers are in modern tradable firms ($x$), modern non-tradable firms ($n$) or traditional/informal self-employment ($u = 1 - x - n$).

**Traditional income.** It is $y_T = P a_T + b\,Y^{nr}$: informal services plus a non-contributory transfer indexed to non-resource GDP per capita.

**Formal labor cost.** Workers take a formal job if $W\,[1-(1-\beta)\tau] \ge y_T$. Here $\tau$ is the payroll wedge and $\beta$ is how much workers value their contributions. If surplus labor is exhausted ($u = u_{min}$), $W$ rises above this level (the Lewis turning point).

**Firms need managers.** $K$ people can run a firm. Each chooses tradable or non-tradable production (logit on profits), or not to run a firm (logit on profit versus $\kappa_m y_T$). Firm output is $A\,\ell^\alpha$ (tradables) or $P\nu A\,\ell^\alpha$ (services), where $A$ is productivity relative to the frontier.

**Government.**

$$\tau\,W(x+n) + \kappa_R\theta_R R^{ret} = g\,Y^{nr} + b\,Y^{nr}u + \text{export subsidy}, \qquad 0 \le \tau \le \tau_{max}.$$

If $\tau$ hits its ceiling, transfers are rationed.

**Rents and ownership.**
- Commodity rent $R$ is an enclave with no workers.
- A share $\rho_R$ of rents and $\rho_F$ of modern profits belongs to foreigners.
- A share $\sigma_R$ of retained rents is spent at home; the rest is saved abroad.

**Market clearing.** $(1-\psi)\,Z = P\,(Y_N + Y_T)$, where domestic absorption $Z$ equals GNI minus savings abroad. Trade then balances by Walras' law.

**Dynamics.**

$$K' = K(1-\delta_K) + \lambda_X x + \lambda_N n + k_0 - \delta_{idle}(1-q)K, \qquad A' = A + (\theta_X x + \theta_N n)(1-A) - g^* A.$$

Modern (especially tradable) jobs create future managers and pull productivity toward the frontier. Idle managers lose capability faster (the ratchet).
