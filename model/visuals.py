"""
WP04 summary figures (V1-V4): the model's main conclusions in four pictures.

  python model/visuals.py            # all (about 10 minutes on 2 cores)
  python model/visuals.py --only V3

Outputs: papers/WP04_trap_model/figures/V*.png and tables/V*.csv
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

SC = HERE / "scenarios"
OUT = HERE.parent / "papers" / "WP04_trap_model"
FIG, TAB = OUT / "figures", OUT / "tables"

# reference palette (dataviz skill): categorical slots 1-3, text tokens, surface
C1, C2, C3 = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#8a8984", "#d9d8d4", "#fcfcfb"
TRAP_FILL = "#cde2fb"
plt.rcParams.update({"font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.titlecolor": INK,
                     "figure.facecolor": SURF, "axes.facecolor": SURF})

BASE = tm.load_scenario(SC / "baseline.toml")
REFORM = tm.deep_update(BASE, {"labor": {"b": 0.08, "beta": 0.7}})
K_RANGE, A_RANGE = (0.02, 0.40), (0.25, 0.90)


def style(ax, title=None):
    if title:
        ax.set_title(title, loc="left", fontsize=10)
    ax.grid(color=GRID, lw=0.6)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def push(value, start=5, end=25):
    return {"events": [{"start": start, "end": end, "section": "government", "param": "sub_X", "value": value}]}


MGR = {"events": [{"start": 5, "end": 20, "section": "dynamics", "param": "k0", "value": 0.005}]}


# ------------------------------------------------------------------ V1 landscape
def _ridge_point(args):
    which, K = args
    p = BASE if which == "base" else REFORM
    att = tm.attractors(p)
    return which, K, tm.ridge(p, [K], att)[0]


def flow(p, nK=14, nA=12):
    Ks = np.linspace(*K_RANGE, nK)
    As = np.linspace(*A_RANGE, nA)
    X, Y, U, V = [], [], [], []
    for A in As:
        P = None
        for K in Ks:
            e = tm.solve_static(p, K, A, 0.0, P_guess=P)
            P = e.P
            K1, A1 = tm.step(p, K, A, e)
            dk, da = (K1 - K) / (K_RANGE[1] - K_RANGE[0]), (A1 - A) / (A_RANGE[1] - A_RANGE[0])
            n = np.hypot(dk, da) or 1.0
            X.append(K); Y.append(A); U.append(dk / n); V.append(da / n)
    return map(np.array, (X, Y, U, V))


def V1(reuse: bool = False):
    Ks = list(np.round(np.linspace(0.02, 0.40, 14), 4))
    cache = TAB / "V1_ridge.csv"
    if reuse and cache.exists():
        rows = list(csv.DictReader(cache.open()))
        Ks = [float(r["K"]) for r in rows]
        ridge_A = np.array([float(r["A_threshold"]) for r in rows])
    else:
        with Pool(2) as pool:
            res = pool.map(_ridge_point, [("base", k) for k in Ks])
        ridge_A = np.array([r[2] for r in res])
    att_b, att_r = tm.attractors(BASE), tm.attractors(REFORM)
    Kt, At, _ = att_b["trap"]
    Km, Am, _ = att_b["modern"]
    paths = {
        "Export push 15% for 20 years": (tm.simulate(tm.deep_update(BASE, push(0.15)), K0=Kt, A0=At), C2),
        "Export push 25% for 20 years": (tm.simulate(tm.deep_update(BASE, push(0.25)), K0=Kt, A0=At), C1),
        "Managers added for 15 years": (tm.simulate(tm.deep_update(BASE, MGR), K0=Kt, A0=At), C3),
    }
    reform_path = tm.simulate(REFORM, K0=Kt, A0=At)
    with (TAB / "V1_ridge.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["K", "A_threshold"])
        w.writerows([[k, round(a, 4)] for k, a in zip(Ks, ridge_A)])

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 5.0), sharey=True)
    for ax, p, title in ((axes[0], BASE, "Today's structure: two basins"),
                         (axes[1], REFORM, "After a social-insurance reform: one basin")):
        X, Y, U, V = flow(p)
        ax.quiver(X, Y, U, V, color=MUTED, alpha=0.55, angles="xy", scale=28, width=0.0028,
                  headwidth=4, headlength=4)
        style(ax, title)
        ax.set_xlim(*K_RANGE)
        ax.set_ylim(*A_RANGE)
        ax.set_xlabel("managerial capability K (people able to run a modern firm)")
    ax = axes[0]
    top = np.where(np.isnan(ridge_A), A_RANGE[1], ridge_A)
    ax.fill_between(Ks, A_RANGE[0], top, color=TRAP_FILL, alpha=0.7, lw=0, zorder=0)
    ax.plot(Ks, top, color=INK, lw=2, zorder=3)
    ax.text(0.28, 0.29, "TRAP BASIN", color="#184f95", fontsize=11, weight="bold")
    ax.text(0.28, 0.62, "MODERN BASIN", color=INK, fontsize=11, weight="bold")
    ax.annotate("the ridge", xy=(Ks[9], top[9]), xytext=(Ks[9] + 0.03, top[9] + 0.07),
                color=INK, fontsize=9, arrowprops=dict(arrowstyle="-", color=INK, lw=0.8))
    order = ["Export push 25% for 20 years", "Managers added for 15 years", "Export push 15% for 20 years"]
    for name in order:
        o, col = paths[name]
        ax.plot(o["K"], o["A"], color=col, lw=2.6 if "15%" in name else 2.2,
                zorder=5 if "15%" in name else 4)
    # direct labels (no legend): leader line in the path's colour, text in ink
    o25 = paths["Export push 25% for 20 years"][0]
    ax.annotate("Starting in the trap: a 25% export push\nfor 20 years crosses the ridge and\n"
                "keeps going after it ends", (o25["K"][30], o25["A"][30]),
                xytext=(0.035, 0.84), fontsize=8, color=INK,
                arrowprops=dict(arrowstyle="-", color=C1, lw=1.2))
    o15 = paths["Export push 15% for 20 years"][0]
    i15 = int(np.argmax(o15["A"]))
    ax.annotate("a 15% push reaches the\nridge, then slides back", (o15["K"][i15], o15["A"][i15]),
                xytext=(0.03, 0.36), fontsize=8, color=INK,
                arrowprops=dict(arrowstyle="-", color=C2, lw=1.2))
    om = paths["Managers added for 15 years"][0]
    im = int(np.argmax(om["K"]))
    ax.annotate("adding managers raises capability,\nbut productivity doesn't follow:\nback to the trap",
                (om["K"][im], om["A"][im]), xytext=(0.15, 0.405), fontsize=8, color=INK,
                arrowprops=dict(arrowstyle="-", color=C3, lw=1.2))
    ax.plot(Kt, At, "o", ms=11, color=INK, zorder=6)
    ax.plot(Km, Am, "s", ms=10, color=INK, zorder=6)
    ax.annotate("trap\n(72% informal)", (Kt, At), xytext=(0.028, 0.47), fontsize=8.5, color=INK)
    ax.annotate("modern state\n(3% informal)", (Km, Am), xytext=(Km + 0.02, Am + 0.04), fontsize=8.5, color=INK)
    ax.set_ylabel("modern productivity A (world frontier = 1)")
    ax = axes[1]
    ax.plot(reform_path["K"], reform_path["A"], color=C1, lw=2.4, zorder=4)
    ax.plot(Kt, At, "o", ms=11, color=INK, zorder=6)
    Kr, Ar, _ = att_r["modern"]
    ax.plot(Kr, Ar, "s", ms=10, color=INK, zorder=6)
    ax.annotate("old trap point", (Kt, At), xytext=(Kt + 0.015, At - 0.09), fontsize=8.5, color=INK)
    ax.annotate("modern state", (Kr, Ar), xytext=(Kr + 0.02, Ar + 0.05), fontsize=8.5, color=INK)
    ax.text(0.03, 0.865, "No ridge: every starting point reaches the modern state",
            fontsize=9, color=INK, weight="bold")
    ax.annotate("same starting point,\nafter reform", (reform_path["K"][4], reform_path["A"][4]),
                xytext=(0.15, 0.50), fontsize=8, color=INK,
                arrowprops=dict(arrowstyle="-", color=INK, lw=0.8))
    fig.text(0.01, 0.005, "Arrows: direction the economy drifts from each point. Reform: payroll-financed "
             "transfers halved (b 0.16→0.08); contributions valued (β 0.5→0.7). trapmodel "
             f"{tm.MODEL_VERSION}, baseline scenario, no commodity rents.", fontsize=7.5, color=INK2)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(FIG / "V1_landscape.png", dpi=160)
    plt.close(fig)
    print("V1 trap", (round(Kt, 3), round(At, 3)), "push15 final u", round(paths["Export push 15% for 20 years"][0]["u"][-1], 3),
          "push25", round(paths["Export push 25% for 20 years"][0]["u"][-1], 3),
          "mgr", round(paths["Managers added for 15 years"][0]["u"][-1], 3), "reform", round(reform_path["u"][-1], 3))


# ------------------------------------------------------------------ V2 crossing curves
def _wedge_point(args):
    which, tau = args
    p = BASE if which == "base" else REFORM
    f = tm.deep_update(p, {"mechanisms": {"fiscal_loop": False}, "government": {"tau_fixed": tau}})
    out = []
    for s in ((0.04, 0.35), (0.35, 0.80)):
        _, _, e = tm.steady_state(f, *s, T=400)
        m = e.x + e.n
        out.append((m, e.spend / (e.W * m)))
    return which, tau, out


def V2(reuse: bool = False):
    cache = TAB / "V2_wedge.csv"
    if not (reuse and cache.exists()):
        taus_b = sorted(set(np.round(np.r_[np.arange(0.0, 0.46, 0.05), np.arange(0.45, 0.601, 0.005)], 4)))
        taus_r = list(np.round(np.arange(0.0, 0.951, 0.05), 3))
        jobs = [("base", t) for t in taus_b] + [("reform", t) for t in taus_r]
        with Pool(2) as pool:
            res = pool.map(_wedge_point, jobs)
        with cache.open("w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["structure", "tau_fixed", "start", "formal_share", "tau_required"])
            for which, tau, out in res:
                for lab, (m, tr) in zip(("low", "high"), out):
                    w.writerow([which, tau, lab, round(m, 4), round(tr, 4)])
    rows = list(csv.DictReader(cache.open()))
    cap = BASE["government"]["tau_max"]

    def series(which, start):
        pts = sorted((float(r["tau_fixed"]), float(r["tau_required"]), float(r["formal_share"]))
                     for r in rows if r["structure"] == which and r["start"] == start)
        return np.array(pts)

    fig, ax = plt.subplots(figsize=(8.6, 5.6))
    ax.plot([0, 0.9], [0, 0.9], color=MUTED, lw=1.2)
    ax.text(0.645, 0.40, "45° line: the wedge firms\nface equals the wedge\nthe budget needs",
            fontsize=7.5, color=INK2, va="bottom")
    ax.axvline(cap, color=INK2, lw=1, ls="--")
    ax.text(cap + 0.008, 0.05, "ceiling on\nthe wedge", fontsize=8, color=INK2)
    for which, col, lab in (("base", C2, "Today's structure"), ("reform", C1, "After social-insurance reform")):
        for k, start in enumerate(("low", "high")):
            d = series(which, start)
            if which == "base":
                d = d[d[:, 0] <= cap + 1e-9]
            ax.plot(d[:, 0], d[:, 1], color=col, lw=2.4, label=lab if k == 0 else None, zorder=3)
    b = series("base", "low")
    m_mod, t_mod = b[0, 2], b[0, 1]
    trap = b[np.isclose(b[:, 0], cap)][0]
    ax.plot(t_mod, t_mod, "s", ms=10, color=INK, zorder=5)
    ax.annotate(f"MODERN equilibrium\nwedge {t_mod:.2f}, formal share {m_mod:.0%}", (t_mod, t_mod),
                xytext=(0.20, 0.03), fontsize=8, color=INK, arrowprops=dict(arrowstyle="-", color=INK, lw=0.8))
    ax.plot(cap, cap, "o", ms=11, color=INK, zorder=5)
    ax.annotate(f"TRAP: the budget would need {trap[1]:.2f},\nso the wedge sits at the ceiling and\n"
                f"transfers are rationed. Formal share {trap[2]:.0%}", (cap, cap),
                xytext=(0.10, 0.70), fontsize=8, color=INK, arrowprops=dict(arrowstyle="-", color=INK, lw=0.8))
    # tipping point: first crossing of F(tau) above the 45-degree line after the modern equilibrium
    tp = None
    for i in range(1, len(b)):
        if b[i - 1, 1] < b[i - 1, 0] and b[i, 1] >= b[i, 0]:
            x0, y0, x1, y1 = b[i - 1, 0], b[i - 1, 1], b[i, 0], b[i, 1]
            w_ = (x0 - y0) / ((x0 - y0) - (x1 - y1))
            tp = x0 + w_ * (x1 - x0)
            break
    if tp is not None:
        ax.plot(tp, tp, "o", ms=10, mfc=SURF, mec=INK, mew=1.8, zorder=5)
        ax.annotate("TIPPING POINT (unstable):\nabove it the wedge spirals up,\nbelow it the economy modernizes",
                    (tp, tp), xytext=(0.55, 0.30), fontsize=8, color=INK,
                    arrowprops=dict(arrowstyle="-", color=INK, lw=0.8))
    r = series("reform", "low")
    ax.plot(r[0, 1], r[0, 1], "s", ms=10, mfc=SURF, mec=C1, mew=2, zorder=5)
    ax.annotate("after reform: one equilibrium,\nwhatever the starting wedge", (0.45, r[3, 1]),
                xytext=(0.40, 0.08), fontsize=8, color=INK, arrowprops=dict(arrowstyle="-", color=INK, lw=0.8))
    # direction of motion along the 45-degree line (today's structure)
    for x0, x1 in ((0.03, 0.11), (0.43, 0.27), (0.535, 0.585)):
        ax.annotate("", xy=(x1, x1), xytext=(x0, x0),
                    arrowprops=dict(arrowstyle="-|>", color=C2, lw=1.8, mutation_scale=12))
    ax.text(0.19, 0.40, "where the budget needs less than firms\nface, the wedge falls toward the\nmodern equilibrium",
            fontsize=7.5, color=INK2, rotation=0)
    style(ax, "The fiscal loop: three equilibria today, one after reform")
    ax.set_xlim(0, 0.9)
    ax.set_ylim(0, 0.9)
    ax.set_xlabel("payroll wedge firms face (held fixed while the economy adjusts)")
    ax.set_ylabel("wedge the budget then needs")
    ax.legend(loc="upper left", frameon=False, fontsize=8.5)
    fig.text(0.01, 0.005, "Long-run outcomes with the wedge held fixed, from two starting points (they differ only "
             "near 0.50).\nReform: payroll-financed transfers b 0.16→0.08; contributions valued β 0.5→0.7. "
             f"trapmodel {tm.MODEL_VERSION}.", fontsize=7, color=INK2)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.savefig(FIG / "V2_fiscal_loop.png", dpi=160)
    plt.close(fig)
    print("V2 modern", round(t_mod, 3), "tipping", None if tp is None else round(tp, 3), "trap need", trap[1])


# ------------------------------------------------------------------ V3 attribution
def V3():
    rows = list(csv.DictReader((TAB / "E3_attribution.csv").open()))
    ref = float(rows[0]["GNI"])
    plain = {
        "LAC-type (reference)": "LAC-type economy (reference)",
        "fiscal loop off (wedge fixed at 0.25)": "Wedge no longer rises as the formal base shrinks",
        "rent absorption off (rents not spent)": "Commodity rents not spent at home",
        "remittances off (all profits national)": "No foreign-owned profits or rents",
        "ratchet off (no extra idle-manager loss)": "Idle managers keep their skills",
        "smaller payroll-financed transfers (b 0.16→0.08)": "Half the transfers financed by payroll",
        "contributions valued (beta 0.4→0.8)": "Workers value their contributions (β 0.4→0.8)",
        "no commodity cycles": "No commodity booms",
        "faster learning in tradables (theta_X ×1.5)": "Exporting firms learn 50% faster",
        "more managers from outside (k0 ×5)": "Five times more managers from schools/FDI",
    }
    data = sorted([(plain[r["change from LAC-type"]], 100 * float(r["GNI"]) / ref, float(r["u"]) < 0.3)
                   for r in rows], key=lambda d: d[1])
    fig, ax = plt.subplots(figsize=(8.5, 4.4))
    y = np.arange(len(data))
    for i, (lab, v, esc) in enumerate(data):
        ax.plot([100, v], [i, i], color=GRID, lw=2, zorder=1)
        ax.plot(v, i, "o", ms=9, color=C1 if esc else SURF, mec=C1 if esc else INK2, mew=1.6, zorder=3)
        ax.text(v + (6 if v >= 100 else -6), i, f"{v:.0f}", va="center", ha="left" if v >= 100 else "right",
                fontsize=8, color=INK)
    ax.set_yticks(y, [d[0] for d in data])
    ax.axvline(100, color=INK2, lw=1)
    ax.set_xlim(80, 290)
    ax.set_xlabel("long-run national income (LAC-type economy = 100)")
    style(ax, "What holds the LAC-type economy back? One change at a time")
    ax.plot([], [], "o", color=C1, ms=8, label="escapes the trap")
    ax.plot([], [], "o", color=SURF, mec=INK2, mew=1.6, ms=8, label="stays in the trap")
    ax.legend(loc="lower right", frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "V3_attribution.png", dpi=160)
    plt.close(fig)


# ------------------------------------------------------------------ V4 ratchet
def V4():
    spent_p = tm.load_scenario(SC / "boom_ratchet.toml")
    saved_p = tm.load_scenario(SC / "boom_ratchet.toml", {"ownership": {"sigma_R": 0.3}})
    noboom_p = tm.load_scenario(SC / "boom_ratchet.toml", {"commodity": {"boom": 0.0}})
    spent, saved = tm.simulate(spent_p), tm.simulate(saved_p)
    att = tm.attractors(noboom_p)
    c = spent_p["commodity"]
    b0, b1 = c["boom_start"], c["boom_start"] + c["boom_length"]
    pnr = None
    for t in range(b0, b1 + 1):            # if the boom stopped here, would it recover?
        if tm.classify(noboom_p, float(spent["K"][t]), float(spent["A"][t]), att) == "trap":
            pnr = t
            break
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.axvspan(b0, b1, color=GRID, alpha=0.6, lw=0)
    ax.text(b0 + 0.3, 0.715, "commodity boom", fontsize=8, color=INK2)
    ax.plot(spent["t"][:60], spent["A"][:60], color=C2, lw=2.4, label="Boom spent at home")
    ax.plot(saved["t"][:60], saved["A"][:60], color=C1, lw=2.4, label="Same boom, 70% saved abroad")
    if pnr is not None:
        ax.axvline(pnr, color=INK, lw=1.2, ls="--")
        ax.annotate(f"point of no return (year {pnr}):\neven if the boom stopped now,\nthe economy would not recover",
                    (pnr, float(spent["A"][pnr])), xytext=(pnr + 4, 0.50), fontsize=8, color=INK,
                    arrowprops=dict(arrowstyle="-", color=INK, lw=0.8))
    ax.text(58, float(spent["A"][59]) + 0.008, "stuck in the trap", ha="right", fontsize=8, color=INK)
    ax.text(58, float(saved["A"][59]) + 0.008, "modern state", ha="right", fontsize=8, color=INK)
    ax.set_xlabel("year")
    ax.set_ylabel("modern productivity A (frontier = 1)")
    ax.set_ylim(0.44, 0.74)
    style(ax, "One boom, two outcomes: an economy just inside the modern basin")
    ax.legend(loc="center right", frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "V4_ratchet.png", dpi=160)
    plt.close(fig)
    print("V4 point of no return", pnr)


FIGS = {"V1": V1, "V2": V2, "V3": V3, "V4": V4}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--reuse", action="store_true", help="reuse cached ridge for V1")
    a = ap.parse_args()
    FIG.mkdir(parents=True, exist_ok=True)
    TAB.mkdir(parents=True, exist_ok=True)
    for k, f in FIGS.items():
        if not a.only or k in a.only:
            print("building", k, flush=True)
            f(a.reuse) if k in ("V1", "V2") else f()
