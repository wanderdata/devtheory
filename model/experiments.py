"""
WP04 experiments. Regenerates every figure and table in the paper.

  python model/experiments.py            # all experiments (a few minutes)
  python model/experiments.py --only E3  # one experiment

Outputs: papers/WP04_trap_model/figures/*.png, tables/*.csv, results.md
"""
from __future__ import annotations

import argparse
import csv
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import trapmodel as tm  # noqa: E402

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402

SC = HERE / "scenarios"
OUT = HERE.parent / "papers" / "WP04_trap_model"
FIG, TAB = OUT / "figures", OUT / "tables"

# reference palette (dataviz skill): categorical slots 1-3, text tokens, blue ramp
C1, C2, C3 = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, GRID = "#0b0b0b", "#52514e", "#d9d8d4"
BLUES = LinearSegmentedColormap.from_list("b", ["#cde2fb", "#86b6ef", "#2a78d6", "#184f95", "#0d366b"])
plt.rcParams.update({"font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.titlecolor": INK,
                     "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb"})

RESULTS: list[str] = []


def style(ax, title):
    ax.set_title(title, loc="left", fontsize=9.5)
    ax.grid(color=GRID, lw=0.6)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def tail_mean(o, k, n=10):
    return float(np.mean(o[k][-n:]))


def write_csv(name, rows, header):
    TAB.mkdir(parents=True, exist_ok=True)
    with (TAB / name).open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)


# ---------------------------------------------------------------- E1 basins
def _basin_cell(args):
    K0, A0 = args
    p = tm.load_scenario(SC / "baseline.toml")
    _, _, e = tm.steady_state(p, K0, A0, T=250)
    return K0, A0, e.u


def E1():
    Ks = np.round(np.linspace(0.02, 0.40, 10), 3)
    As = np.round(np.linspace(0.30, 0.80, 11), 3)
    with Pool(2) as pool:
        res = pool.map(_basin_cell, [(k, a) for a in As for k in Ks])
    U = np.array([r[2] for r in res]).reshape(len(As), len(Ks))
    write_csv("E1_basins.csv", [[k, a, round(u, 4)] for k, a, u in res], ["K0", "A0", "final_u"])
    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    im = ax.imshow(U, origin="lower", aspect="auto", cmap=BLUES, vmin=0, vmax=0.8,
                   extent=[Ks[0], Ks[-1], As[0], As[-1]])
    cb = fig.colorbar(im, ax=ax, shrink=0.85)
    cb.set_label("long-run traditional/informal share")
    ax.set_xlabel("initial managerial capability K")
    ax.set_ylabel("initial modern productivity A (frontier = 1)")
    style(ax, "E1. Basins of attraction (baseline): trap vs. modern steady state")
    ax.text(0.05, 0.33, "TRAP", color="#fcfcfb", fontsize=12, weight="bold")
    ax.text(0.30, 0.74, "MODERN", color=INK, fontsize=12, weight="bold")
    fig.tight_layout()
    fig.savefig(FIG / "E1_basins.png", dpi=150)
    plt.close(fig)
    trapped = (U > 0.4).mean()
    RESULTS.append(f"- **E1.** Share of the (K0, A0) grid that ends in the trap: {trapped:.0%}. "
                   f"Trap steady state u ≈ {U.max():.2f}; modern steady state u ≈ {U.min():.2f}.")


# ---------------------------------------------------------------- E2 scenarios
def E2():
    names = [("lac_type", "LAC-type", C2), ("escaper", "Escaper", C1),
             ("resource_rich_advanced", "Resource-rich advanced", C3)]
    runs = {n: tm.simulate(tm.load_scenario(SC / f"{n}.toml")) for n, _, _ in names}
    fig, axes = plt.subplots(2, 2, figsize=(9, 6), sharex=True)
    panels = [("u", "Traditional / informal share"), ("A", "Modern productivity (frontier = 1)"),
              ("tau", "Payroll wedge on formal labor"), ("GNI", "National income per worker")]
    for ax, (k, lab) in zip(axes.flat, panels):
        for n, lbl, col in names:
            ax.plot(runs[n]["t"], runs[n][k], color=col, lw=2, label=lbl)
        style(ax, lab)
    axes[1, 0].set_xlabel("year")
    axes[1, 1].set_xlabel("year")
    axes[0, 0].legend(frameon=False, fontsize=8.5)
    fig.tight_layout()
    fig.savefig(FIG / "E2_scenarios.png", dpi=150)
    plt.close(fig)
    rows = []
    for n, lbl, _ in names:
        o = runs[n]
        rows.append([lbl, round(tail_mean(o, "u"), 3), round(tail_mean(o, "A"), 3),
                     round(tail_mean(o, "tau"), 3), round(tail_mean(o, "GDP"), 3),
                     round(tail_mean(o, "GNI"), 3)])
    write_csv("E2_scenarios.csv", rows, ["scenario", "u", "A", "tau", "GDP", "GNI"])
    ratio = rows[1][5] / rows[0][5]
    RESULTS.append(f"- **E2.** From the same start (K=0.10, A=0.50), the escaper ends with national income "
                   f"{ratio:.1f}× the LAC-type; LAC-type long-run u = {rows[0][1]}, A = {rows[0][2]}; "
                   f"escaper u = {rows[1][1]}, A = {rows[1][2]}.")


# ---------------------------------------------------------------- E3 attribution
LEVERS = [
    ("LAC-type (reference)", {}),
    ("fiscal loop off (wedge fixed at 0.25)", {"mechanisms": {"fiscal_loop": False}}),
    ("rent absorption off (rents not spent)", {"mechanisms": {"rent_absorption": False}}),
    ("remittances off (all profits national)", {"mechanisms": {"remittances": False}}),
    ("ratchet off (no extra idle-manager loss)", {"mechanisms": {"ratchet": False}}),
    ("smaller payroll-financed transfers (b 0.16→0.08)", {"labor": {"b": 0.08}}),
    ("contributions valued (beta 0.4→0.8)", {"labor": {"beta": 0.8}}),
    ("no commodity cycles", {"commodity": {"boom": 0.0, "R_bar": 0.0}}),
    ("faster learning in tradables (theta_X ×1.5)", {"dynamics": {"theta_X": 0.30}}),
    ("more managers from outside (k0 ×5)", {"dynamics": {"k0": 0.0025}}),
]


def _lever(args):
    name, ov = args
    o = tm.simulate(tm.load_scenario(SC / "lac_type.toml", ov))
    return [name, round(tail_mean(o, "u"), 3), round(tail_mean(o, "A"), 3),
            round(tail_mean(o, "tau"), 3), round(tail_mean(o, "GNI"), 3)]


def E3():
    with Pool(2) as pool:
        rows = pool.map(_lever, LEVERS)
    write_csv("E3_attribution.csv", rows, ["change from LAC-type", "u", "A", "tau", "GNI"])
    ref = rows[0][4]
    lines = ["| Change (one at a time, from t = 0) | Long-run informal share | Productivity A | Wedge | National income (LAC-type = 100) |",
             "|---|---:|---:|---:|---:|"]
    for r in rows:
        lines.append(f"| {r[0]} | {r[1]:.2f} | {r[2]:.2f} | {r[3]:.2f} | {100 * r[4] / ref:.0f} |")
    (TAB / "E3_attribution.md").write_text("\n".join(lines) + "\n")
    esc = [r[0] for r in rows[1:] if r[1] < 0.3]
    RESULTS.append("- **E3.** Single changes that let the LAC-type escape: " + ("; ".join(esc) if esc else "none") + ".")


# ---------------------------------------------------------------- E4 policy from inside the trap
def _policy(args):
    name, events, perm, K0, A0 = args
    ov = tm.deep_update({"commodity": {"boom": 0.0}, "events": events}, perm)
    p = tm.load_scenario(SC / "lac_type.toml", ov)
    o = tm.simulate(p, K0=K0, A0=A0)
    return name, o


def E4():
    lac = tm.simulate(tm.load_scenario(SC / "lac_type.toml"))
    K0, A0 = float(lac["K"][-1]), float(lac["A"][-1])
    push = [{"start": 5, "end": 25, "section": "government", "param": "sub_X", "value": 0.15}]
    bigpush = [dict(push[0], value=0.40)]
    mgr = [{"start": 5, "end": 20, "section": "dynamics", "param": "k0", "value": 0.005}]
    wedge = {"labor": {"b": 0.08, "beta": 0.7}}
    cases = [
        ("No change", [], {}),
        ("A. Wedge reform (permanent)", [], wedge),
        ("B. Export push (20 years)", push, {}),
        ("B'. Large export push (40%, 20 years)", bigpush, {}),
        ("C. Manager/FDI injection (15 years)", mgr, {}),
        ("A + B", push, wedge),
        ("A + C", mgr, wedge),
        ("B + C", push + mgr, {}),
    ]
    with Pool(2) as pool:
        res = pool.map(_policy, [(n, ev, pm, K0, A0) for n, ev, pm in cases])
    rows = [[n, round(tail_mean(o, "u"), 3), round(tail_mean(o, "A"), 3), round(tail_mean(o, "GNI"), 3)]
            for n, o in res]
    write_csv("E4_policy.csv", rows, ["package", "u", "A", "GNI"])
    ref = rows[0][3]
    lines = ["| Package (starting inside the LAC-type trap) | Long-run informal share | Productivity A | National income (no change = 100) |",
             "|---|---:|---:|---:|"]
    for r in rows:
        lines.append(f"| {r[0]} | {r[1]:.2f} | {r[2]:.2f} | {100 * r[3] / ref:.0f} |")
    (TAB / "E4_policy.md").write_text("\n".join(lines) + "\n")
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.6), sharex=True)
    show = {"No change": INK2, "A. Wedge reform (permanent)": C2, "B. Export push (20 years)": C3,
            "B'. Large export push (40%, 20 years)": C1}
    for n, o in res:
        if n in show:
            axes[0].plot(o["t"], o["u"], color=show[n], lw=2, label=n)
            axes[1].plot(o["t"], o["GNI"], color=show[n], lw=2, label=n)
    style(axes[0], "Traditional / informal share")
    style(axes[1], "National income per worker")
    for ax in axes:
        ax.set_xlabel("year")
    axes[0].legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "E4_policy.png", dpi=150)
    plt.close(fig)
    bp = dict(res)["B'. Large export push (40%, 20 years)"]
    RESULTS.append(f"- **E4 (cost).** During the large push the wedge is capped, so transfers to informal "
                   f"workers are rationed: minimum b_eff = {float(bp['b_eff'].min()):.3f} vs. 0.16 target.")
    esc = [r[0] for r in rows if r[1] < 0.3]
    RESULTS.append(f"- **E4.** Starting from the LAC-type trap (K={K0:.3f}, A={A0:.2f}), packages that escape: "
                   + ("; ".join(esc) if esc else "none") + ".")


# ---------------------------------------------------------------- E5 ratchet
def E5():
    cases = [("Boom spent at home", {}, C2), ("Same boom, 70% saved abroad", {"ownership": {"sigma_R": 0.3}}, C1),
             ("No boom", {"commodity": {"boom": 0.0}}, INK2)]
    runs = [(n, tm.simulate(tm.load_scenario(SC / "boom_ratchet.toml", ov)), c) for n, ov, c in cases]
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.4), sharex=True)
    for n, o, c in runs:
        axes[0].plot(o["t"], o["R"], color=c, lw=2, label=n)
        axes[1].plot(o["t"], o["u"], color=c, lw=2)
        axes[2].plot(o["t"], o["A"], color=c, lw=2)
    style(axes[0], "Commodity rent")
    style(axes[1], "Traditional / informal share")
    style(axes[2], "Modern productivity A")
    for ax in axes:
        ax.set_xlabel("year")
        ax.axvspan(3, 15, color=GRID, alpha=0.5, lw=0)
    axes[0].legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "E5_ratchet.png", dpi=150)
    plt.close(fig)
    rows = [[n, round(tail_mean(o, "u"), 3), round(float(o["A"].min()), 3), round(tail_mean(o, "GNI"), 3)]
            for n, o, _ in runs]
    write_csv("E5_ratchet.csv", rows, ["case", "long_run_u", "min_A", "long_run_GNI"])
    RESULTS.append(f"- **E5.** Near the threshold (K=0.08, A=0.66): boom spent → long-run u = {rows[0][1]}; "
                   f"70% saved → u = {rows[1][1]}; no boom → u = {rows[2][1]}. Long-run national income spent/no-boom = "
                   f"{rows[0][3] / rows[2][3]:.2f}.")


EXPERIMENTS = {"E1": E1, "E2": E2, "E3": E3, "E4": E4, "E5": E5}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args()
    FIG.mkdir(parents=True, exist_ok=True)
    TAB.mkdir(parents=True, exist_ok=True)
    for k, f in EXPERIMENTS.items():
        if a.only and k not in a.only:
            continue
        print("running", k, flush=True)
        f()
    if not a.only:
        (OUT / "results.md").write_text(
            f"# WP04 results (auto-generated by model/experiments.py, trapmodel {tm.MODEL_VERSION})\n\n"
            + "\n".join(RESULTS) + "\n")
    print("\n".join(RESULTS))


if __name__ == "__main__":
    main()
