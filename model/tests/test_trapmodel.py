"""Accounting and behaviour tests. Run: python -m pytest model/tests -q"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import trapmodel as tm  # noqa: E402

SC = Path(__file__).resolve().parents[1] / "scenarios"
STATES = [(0.05, 0.4, 0.0), (0.10, 0.5, 0.06), (0.30, 0.75, 0.04), (0.08, 0.66, 0.12)]


@pytest.mark.parametrize("K,A,R", STATES)
@pytest.mark.parametrize("scen", ["baseline", "lac_type", "escaper", "resource_rich_advanced"])
def test_static_accounting(scen, K, A, R):
    p = tm.load_scenario(SC / f"{scen}.toml")
    e = tm.solve_static(p, K, A, R)
    assert abs(e.excess_N) < 1e-8                     # non-tradable market clears
    assert abs(e.trade_gap) < 1e-8                    # trade balances (Walras)
    assert abs(e.x + e.n + e.u - 1) < 1e-12           # labor adds up
    assert e.u >= p["labor"]["u_min"] - 1e-9
    assert abs(e.rev - e.spend) < 1e-7                # government budget balances
    assert 0 <= e.tau <= p["government"]["tau_max"] + 1e-12
    assert e.GNI <= e.GDP + 1e-12


def test_trap_and_escape_from_same_start():
    lac = tm.simulate(tm.load_scenario(SC / "lac_type.toml"))
    esc = tm.simulate(tm.load_scenario(SC / "escaper.toml"))
    assert lac["u"][-1] > 0.6 and esc["u"][-1] < 0.1
    assert esc["GDP"][-1] > 2 * lac["GDP"][-1]


def test_two_steady_states_in_baseline():
    p = tm.load_scenario(SC / "baseline.toml")
    _, _, lo = tm.steady_state(p, 0.02, 0.3, T=250)
    _, _, hi = tm.steady_state(p, 0.3, 0.75, T=250)
    assert lo.u - hi.u > 0.5


def test_conditional_ratchet():
    spent = tm.simulate(tm.load_scenario(SC / "boom_ratchet.toml"))
    saved = tm.simulate(tm.load_scenario(SC / "boom_ratchet.toml", {"ownership": {"sigma_R": 0.3}}))
    assert spent["u"][-1] > 0.6 and saved["u"][-1] < 0.1


def test_switches_run():
    p = tm.load_scenario(SC / "lac_type.toml")
    for m in p["mechanisms"]:
        q = tm.deep_update(p, {"mechanisms": {m: False}, "simulation": {"T": 20}})
        tm.simulate(q)
