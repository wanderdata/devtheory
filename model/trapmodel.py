"""
trapmodel — a minimal model of a middle-income "segment trap" (devtheory WP04).

Version: see MODEL_VERSION. Equations are documented in model/README.md and WP04.

Economy (small, open, labor force = 1, everything in units of the tradable good):

  Segments
    x  : modern tradable employment      (firms sell abroad at world price 1)
    n  : modern non-tradable employment  (firms sell domestic services at price P)
    u  : traditional / informal          (self-employed, productivity a_T in services)

  State variables (slow-moving)
    K  : managerial capability = number of people able to run a modern firm
    A  : modern productivity relative to the world frontier (0 < A < 1)
    R  : commodity rent (exogenous path; enclave sector with no labor)

  Each period: given (K, A, R) solve for the non-tradable price P, the payroll
  wedge tau and the modern wage W such that the non-tradable market clears, the
  government budget balances and labor adds up. Then K and A evolve.

Mechanisms (each can be switched off in the scenario file, [mechanisms] table)
  capability_loop : modern jobs (especially tradable ones) create future managers
  learning_loop   : tradable employment speeds catch-up to the frontier
  fiscal_loop     : informal workers' benefits and public goods are financed by a
                    payroll wedge on formal jobs; a small formal base -> high wedge
  rent_absorption : commodity rents spent at home raise P (Dutch disease)
  ratchet         : idle managers lose capability faster than it is rebuilt
  remittances     : foreign-owned profits and rents leave the country
"""
from __future__ import annotations

import copy
import math
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

MODEL_VERSION = "0.1.0"

# ----------------------------------------------------------------------------
# Parameters
# ----------------------------------------------------------------------------

DEFAULTS = {
    "technology": {
        "alpha": 0.65,      # curvature of modern firm output A*l^alpha (span of control)
        "a_T": 0.25,        # traditional productivity (service units per worker)
        "nu": 1.8,          # modern non-tradable productivity relative to A
        "psi": 0.40,        # tradable share of spending
    },
    "labor": {
        "beta": 0.5,        # value workers place on payroll contributions (0..1)
        "b": 0.16,          # non-contributory benefit per traditional worker, share of non-resource GDP pc
        "u_min": 0.03,      # irreducible traditional share
    },
    "government": {
        "g": 0.10,          # public goods, share of non-resource GDP, financed with b by the payroll wedge
        "theta_R": 0.5,     # share of retained commodity rent taken by the state
        "kappa_R": 0.0,     # share of the state's rent used to cut the payroll wedge
                            # (rest funds extra spending: procyclical fiscal policy)
        "tau_max": 0.60,    # ceiling on the payroll wedge
        "tau_fixed": 0.25,  # wedge used when fiscal_loop is off
        "sub_X": 0.0,       # subsidy rate on tradable modern output (export promotion)
    },
    "managers": {
        "eta_alloc": 4.0,   # sharpness of managers' choice between X and N firms
        "eta_part": 4.0,    # sharpness of participation (run a firm vs. not)
        "kappa_m": 2.0,     # manager outside option, multiple of traditional income
    },
    "dynamics": {
        "delta_K": 0.04,    # depreciation of capability (retirement)
        "delta_idle": 0.10, # extra depreciation of idle managers' capability (ratchet)
        "lam_X": 0.020,     # managers created per worker-year in modern tradable jobs
        "lam_N": 0.008,     # ... in modern non-tradable jobs
        "k0": 0.0005,       # managers from outside the modern sector (education, FDI)
        "theta_X": 0.20,    # catch-up speed per unit of tradable modern employment
        "theta_N": 0.03,    # ... per unit of non-tradable modern employment
        "g_star": 0.040,    # frontier drift (relative A erodes without catch-up)
    },
    "ownership": {
        "rho_F": 0.0,       # share of modern profits remitted abroad
        "rho_R": 0.0,       # share of commodity rent owned abroad
        "sigma_R": 1.0,     # share of retained rent spent at home (rest saved abroad)
        "phi_off": 0.0,     # share of domestic profits moved offshore
    },
    "commodity": {
        "R_bar": 0.0,       # baseline rent (share of tradable units per capita)
        "boom": 0.0,        # boom size added on top of R_bar
        "boom_start": 20,
        "boom_length": 10,
        "cycles": 1,        # number of boom-bust cycles
        "cycle_gap": 25,    # years between boom starts
    },
    "initial": {"K": 0.05, "A": 0.35},
    "simulation": {"T": 120},
    "mechanisms": {
        "capability_loop": True,
        "learning_loop": True,
        "fiscal_loop": True,
        "rent_absorption": True,
        "ratchet": True,
        "remittances": True,
    },
    "events": [],           # list of {start, end, section, param, value}
}


def deep_update(base: dict, upd: dict) -> dict:
    out = copy.deepcopy(base)
    for k, v in upd.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_update(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out


def load_scenario(path: str | Path, overrides: dict | None = None) -> dict:
    """Load a TOML scenario on top of DEFAULTS. A scenario may 'inherit' another file."""
    path = Path(path)
    with path.open("rb") as fh:
        sc = tomllib.load(fh)
    base = DEFAULTS
    if "inherit" in sc:
        base = load_scenario(path.parent / sc.pop("inherit"))
    p = deep_update(base, sc)
    if overrides:
        p = deep_update(p, overrides)
    return p


def params_at(p: dict, t: int) -> dict:
    """Apply time-limited policy events active in period t."""
    q = p
    for ev in p.get("events", []):
        if ev["start"] <= t < ev.get("end", 10**9):
            if q is p:
                q = copy.deepcopy(p)
            q[ev["section"]][ev["param"]] = ev["value"]
    return q


def rent_path(p: dict) -> np.ndarray:
    c, T = p["commodity"], p["simulation"]["T"]
    R = np.full(T, float(c["R_bar"]))
    for k in range(int(c["cycles"])):
        s = int(c["boom_start"] + k * c["cycle_gap"])
        R[s:s + int(c["boom_length"])] += c["boom"]
    return R


# ----------------------------------------------------------------------------
# Static equilibrium
# ----------------------------------------------------------------------------

@dataclass
class Eq:
    P: float; W: float; tau: float; b_eff: float
    s: float; q: float; x: float; n: float; u: float
    Y_X: float; Y_N: float; Y_T: float; GDP: float; GNI: float; Z: float
    profits: float; remitted: float; saved_abroad: float
    rev: float; spend: float; trade_gap: float
    excess_N: float = 0.0
    info: dict = field(default_factory=dict)


def _firm_block(p, K, A, P, W):
    """Given prices, return per-firm labor, profits, allocation and employment."""
    tech, man, gov = p["technology"], p["managers"], p["government"]
    al = tech["alpha"]
    AX = (1.0 + gov["sub_X"]) * A
    AN = P * tech["nu"] * A
    lX = (al * AX / W) ** (1.0 / (1.0 - al))
    lN = (al * AN / W) ** (1.0 / (1.0 - al))
    piX = (1.0 / al - 1.0) * W * lX          # profit = A l^a - W l = W l (1/a - 1)
    piN = (1.0 / al - 1.0) * W * lN
    s = 1.0 / (1.0 + (piN / piX) ** man["eta_alloc"])
    pibar = s * piX + (1.0 - s) * piN
    return lX, lN, piX, piN, s, pibar


def solve_static(p: dict, K: float, A: float, R: float, tau_guess: float = 0.2,
                 P_guess: float | None = None) -> Eq:
    tech, lab, gov, own, mech = (p["technology"], p["labor"], p["government"],
                                 p["ownership"], p["mechanisms"])
    al, aT, psi = tech["alpha"], tech["a_T"], tech["psi"]
    beta, b, u_min = lab["beta"], lab["b"], lab["u_min"]
    rhoF = own["rho_F"] if mech["remittances"] else 0.0
    rhoR = own["rho_R"] if mech["remittances"] else 0.0
    R_ret = (1.0 - rhoR) * R
    sigmaR = own["sigma_R"] if mech["rent_absorption"] else 0.0
    m_cap = 1.0 - u_min

    def inner(P):
        """For given P, find (tau, b_eff, W) consistent with budget and labor."""
        tau, b_eff, GDP = tau_guess, b, None
        for _ in range(300):
            if GDP is None:
                GDP = P * aT + R                     # first guess
            outside = P * aT + b_eff * (GDP - R)    # traditional income incl. benefit
            W0 = outside / (1.0 - (1.0 - beta) * tau)

            def m_of(W):
                lX, lN, piX, piN, s, pibar = _firm_block(p, K, A, P, W)
                qq = 1.0 / (1.0 + (p["managers"]["kappa_m"] * outside / pibar) ** p["managers"]["eta_part"])
                return K * qq * (s * lX + (1.0 - s) * lN)

            W = W0
            if m_of(W0) > m_cap:              # Lewis turning point: surplus labor exhausted
                W = brentq(lambda w: m_of(w) - m_cap, W0, W0 * 1e4)
            lX, lN, piX, piN, s, pibar = _firm_block(p, K, A, P, W)
            q = 1.0 / (1.0 + (p["managers"]["kappa_m"] * outside / pibar) ** p["managers"]["eta_part"])
            x = K * q * s * lX
            n = K * q * (1.0 - s) * lN
            m = x + n
            u = 1.0 - m
            subsidy = gov["sub_X"] * A * K * q * s * lX ** al
            GDP_new = (A * K * q * s * lX ** al
                       + P * (tech["nu"] * A * K * q * (1.0 - s) * lN ** al + aT * u) + R)
            Ynr = GDP_new - R                       # non-resource GDP: base for spending rules
            need = (gov["g"] * Ynr + b_eff * Ynr * u + subsidy
                    - gov["kappa_R"] * gov["theta_R"] * R_ret)
            if mech["fiscal_loop"]:
                tau_new = need / (W * m) if m > 1e-12 else gov["tau_max"]
                tau_new = min(max(tau_new, 0.0), gov["tau_max"])
            else:
                tau_new = gov["tau_fixed"]
            # if the wedge is capped, benefits are rationed to balance the budget
            if mech["fiscal_loop"] and tau_new >= gov["tau_max"] - 1e-12:
                avail = (gov["tau_max"] * W * m + gov["kappa_R"] * gov["theta_R"] * R_ret
                         - gov["g"] * Ynr - subsidy)
                b_new = min(b, max(avail, 0.0) / max(Ynr * u, 1e-12))
            else:
                b_new = b
            if (abs(tau_new - tau) < 1e-11 and abs(b_new - b_eff) < 1e-11
                    and abs(GDP_new - GDP) < 1e-11 * max(1.0, GDP)):
                break
            tau = 0.5 * tau + 0.5 * tau_new
            b_eff = 0.5 * b_eff + 0.5 * b_new
            GDP = 0.5 * GDP + 0.5 * GDP_new
        return dict(tau=tau, b_eff=b_eff, W=W, lX=lX, lN=lN, piX=piX, piN=piN, s=s, q=q,
                    x=x, n=n, u=u, subsidy=subsidy, outside=outside)

    def accounts(P, r):
        Y_X = A * K * r["q"] * r["s"] * r["lX"] ** al                 # at world price
        Y_N = tech["nu"] * A * K * r["q"] * (1 - r["s"]) * r["lN"] ** al
        Y_T = aT * r["u"]
        profits = K * r["q"] * (r["s"] * r["piX"] + (1 - r["s"]) * r["piN"])  # incl. subsidy
        GDP = Y_X + P * (Y_N + Y_T) + R
        remitted = rhoF * profits + rhoR * R
        GNI = GDP - remitted
        saved = (1.0 - sigmaR) * R_ret + own["phi_off"] * (1 - rhoF) * profits
        Z = GNI - saved                                                # domestic absorption
        excess = (1.0 - psi) * Z / P - (Y_N + Y_T)
        return dict(Y_X=Y_X, Y_N=Y_N, Y_T=Y_T, profits=profits, GDP=GDP, GNI=GNI,
                    remitted=remitted, saved=saved, Z=Z, excess=excess)

    def excess_of_logP(lp):
        P = math.exp(lp)
        return accounts(P, inner(P))["excess"]

    root = None
    if P_guess is not None:                       # warm start: expand a bracket around last P
        c, w = math.log(P_guess), 0.05
        while w < 8 and root is None:
            a_, b_ = c - w, c + w
            fa, fb = excess_of_logP(a_), excess_of_logP(b_)
            if fa > 0 >= fb:
                root = brentq(excess_of_logP, a_, b_, xtol=1e-12)
            w *= 2.5
    if root is None:                              # global search on a log grid
        lo, hi = math.log(1e-3), math.log(1e3)
        grid = np.linspace(lo, hi, 61)
        vals = [excess_of_logP(g) for g in grid]
        for i in range(len(grid) - 1):
            if vals[i] > 0 >= vals[i + 1]:
                root = brentq(excess_of_logP, grid[i], grid[i + 1], xtol=1e-12)
                break
    if root is None:
        raise RuntimeError("non-tradable market did not clear on the price grid")
    P = math.exp(root)
    r = inner(P)
    a = accounts(P, r)
    rev = r["tau"] * r["W"] * (r["x"] + r["n"]) + p["government"]["theta_R"] * R_ret
    Ynr = a["GDP"] - R
    spend = (p["government"]["g"] * Ynr + r["b_eff"] * Ynr * r["u"] + r["subsidy"]
             + (1.0 - p["government"]["kappa_R"]) * p["government"]["theta_R"] * R_ret)
    surplus = 0.0
    if r["tau"] <= 1e-9 and rev > spend:          # rents exceed needs: surplus spent publicly
        surplus = rev - spend
        spend = rev
    # tradable balance: demand psi*Z vs exports + rents - remittances - savings abroad
    trade_gap = psi * a["Z"] - (a["Y_X"] + R - a["remitted"] - a["saved"])
    return Eq(P=P, W=r["W"], tau=r["tau"], b_eff=r["b_eff"], s=r["s"], q=r["q"],
              x=r["x"], n=r["n"], u=r["u"], Y_X=a["Y_X"], Y_N=a["Y_N"], Y_T=a["Y_T"],
              GDP=a["GDP"], GNI=a["GNI"], Z=a["Z"], profits=a["profits"],
              remitted=a["remitted"], saved_abroad=a["saved"], rev=rev, spend=spend,
              trade_gap=trade_gap, excess_N=a["excess"],
              info=dict(lX=r["lX"], lN=r["lN"], piX=r["piX"], piN=r["piN"], surplus=surplus))


# ----------------------------------------------------------------------------
# Dynamics
# ----------------------------------------------------------------------------

def step(p: dict, K: float, A: float, e: Eq) -> tuple[float, float]:
    d, mech = p["dynamics"], p["mechanisms"]
    if mech["capability_loop"]:
        idle = (1.0 - e.q) * K
        K1 = (K + d["lam_X"] * e.x + d["lam_N"] * e.n + d["k0"]
              - d["delta_K"] * K - (d["delta_idle"] * idle if mech["ratchet"] else 0.0))
    else:
        K1 = K
    if mech["learning_loop"]:
        A1 = A + (d["theta_X"] * e.x + d["theta_N"] * e.n) * (1.0 - A) - d["g_star"] * A
    else:
        A1 = A
    return max(K1, 1e-6), min(max(A1, 1e-4), 0.999)


COLUMNS = ["t", "K", "A", "R", "P", "W", "tau", "b_eff", "q", "s", "x", "n", "u",
           "GDP", "GNI", "Z", "Y_X", "remitted", "saved_abroad", "rev", "spend", "trade_gap"]


def simulate(p: dict, K0: float | None = None, A0: float | None = None) -> dict[str, np.ndarray]:
    T = p["simulation"]["T"]
    R = rent_path(p)
    K = p["initial"]["K"] if K0 is None else K0
    A = p["initial"]["A"] if A0 is None else A0
    out = {c: np.zeros(T) for c in COLUMNS}
    tau, P = 0.2, None
    for t in range(T):
        pt = params_at(p, t)
        e = solve_static(pt, K, A, R[t], tau_guess=tau, P_guess=P)
        tau, P = e.tau, e.P
        row = dict(t=t, K=K, A=A, R=R[t], P=e.P, W=e.W, tau=e.tau, b_eff=e.b_eff, q=e.q,
                   s=e.s, x=e.x, n=e.n, u=e.u, GDP=e.GDP, GNI=e.GNI, Z=e.Z, Y_X=e.Y_X,
                   remitted=e.remitted, saved_abroad=e.saved_abroad, rev=e.rev,
                   spend=e.spend, trade_gap=e.trade_gap)
        for c in COLUMNS:
            out[c][t] = row[c]
        K, A = step(pt, K, A, e)
    return out


def steady_state(p: dict, K0: float, A0: float, T: int = 400, R: float | None = None):
    """Iterate with constant rent until convergence; returns final (K, A, Eq)."""
    R = p["commodity"]["R_bar"] if R is None else R
    K, A, tau, P = K0, A0, 0.2, None
    for _ in range(T):
        e = solve_static(p, K, A, R, tau_guess=tau, P_guess=P)
        tau, P = e.tau, e.P
        K1, A1 = step(p, K, A, e)
        if abs(K1 - K) < 1e-9 and abs(A1 - A) < 1e-9:
            K, A = K1, A1
            break
        K, A = K1, A1
    return K, A, solve_static(p, K, A, R, tau_guess=tau, P_guess=P)
