"""
Precompute data for the interactive Trap Explorer (model/explorer/index.html).

  python model/explorer_data.py      # about 25 minutes on 2 cores

Writes model/explorer/explorer_data.json. Sliders on the page snap to the grid below.
"""
from __future__ import annotations

import json
import sys
from itertools import product
from multiprocessing import Pool
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import trapmodel as tm  # noqa: E402

GRID = {
    "b": [0.06, 0.10, 0.13, 0.16, 0.20],        # payroll-financed transfer per informal worker
    "beta": [0.3, 0.5, 0.7],                     # value workers place on contributions
    "theta_X": [0.15, 0.20, 0.30],               # learning speed in exporting firms
}
KS = [round(k, 3) for k in np.linspace(0.02, 0.40, 10)]
FLOW_K = np.linspace(0.03, 0.39, 12)
FLOW_A = np.linspace(0.30, 0.86, 10)
YEARS = 80
STARTS = {"stuck": (0.09, 0.53), "near": (0.08, 0.66), "modern": (0.25, 0.70)}
SHOCKS = {
    "none": {},
    "push15": {"events": [{"start": 3, "end": 23, "section": "government", "param": "sub_X", "value": 0.15}]},
    "push30": {"events": [{"start": 3, "end": 23, "section": "government", "param": "sub_X", "value": 0.30}]},
    "boom_spent": {"commodity": {"boom": 0.12, "boom_start": 3, "boom_length": 12, "cycles": 1},
                   "government": {"kappa_R": 0.0}, "ownership": {"sigma_R": 1.0}},
    "boom_saved": {"commodity": {"boom": 0.12, "boom_start": 3, "boom_length": 12, "cycles": 1},
                   "government": {"kappa_R": 0.0}, "ownership": {"sigma_R": 0.3}},
}
BASE = tm.load_scenario(HERE / "scenarios" / "baseline.toml")


def r3(x):
    return [round(float(v), 3) for v in x]


def combo(args):
    b, beta, th = args
    p = tm.deep_update(BASE, {"labor": {"b": b, "beta": beta}, "dynamics": {"theta_X": th},
                              "simulation": {"T": YEARS}})
    att = tm.attractors(p)
    rid = tm.ridge(p, KS, att) if att["multiple"] else [None] * len(KS)
    rid = [None if (r is None or np.isnan(r)) else round(r, 3) for r in rid]
    flow = []
    for A in FLOW_A:
        P = None
        for K in FLOW_K:
            e = tm.solve_static(p, K, A, 0.0, P_guess=P)
            P = e.P
            K1, A1 = tm.step(p, K, A, e)
            flow.append([round(float(K), 3), round(float(A), 3), round(K1 - K, 5), round(A1 - A, 5)])
    ends = {}
    for which in ("trap", "modern"):
        K, A, _ = att[which]
        _, _, e = tm.steady_state(p, K, A, T=50)
        ends[which] = {"K": round(K, 3), "A": round(A, 3), "u": round(e.u, 3), "GNI": round(e.GNI, 3)}
    paths = {}
    for sname, (K0, A0) in STARTS.items():
        for shname, ov in SHOCKS.items():
            o = tm.simulate(tm.deep_update(p, ov), K0=K0, A0=A0)
            paths[f"{sname}|{shname}"] = {"K": r3(o["K"]), "A": r3(o["A"]), "u": r3(o["u"]),
                                          "GNI": r3(o["GNI"]), "R": r3(o["R"])}
    key = f"{b}|{beta}|{th}"
    return key, {"multiple": bool(att["multiple"]), "ridge": rid, "flow": flow, "ends": ends, "paths": paths}


def main():
    combos = list(product(GRID["b"], GRID["beta"], GRID["theta_X"]))
    out = {"model_version": tm.MODEL_VERSION, "grid": GRID, "K": KS, "years": YEARS,
           "starts": STARTS, "shocks": list(SHOCKS), "data": {}}
    with Pool(2) as pool:
        for i, (key, val) in enumerate(pool.imap_unordered(combo, combos), 1):
            out["data"][key] = val
            print(f"{i}/{len(combos)} {key} multiple={val['multiple']}", flush=True)
    dest = HERE / "explorer" / "explorer_data.json"
    dest.parent.mkdir(exist_ok=True)
    dest.write_text(json.dumps(out, separators=(",", ":")))
    print("wrote", dest, dest.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
