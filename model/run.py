"""
Run one scenario and save its time paths.

  python model/run.py model/scenarios/lac_type.toml
  python model/run.py model/scenarios/lac_type.toml --set labor.b=0.08 --set initial.A=0.6
  python model/run.py model/scenarios/lac_type.toml --switch fiscal_loop=off

Outputs go to model/output/<scenario>[__<tag>]/paths.csv and paths.png.
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import trapmodel as tm  # noqa: E402

PLOT_VARS = [("u", "Traditional / informal share"), ("A", "Modern productivity (frontier = 1)"),
             ("tau", "Payroll wedge"), ("GDP", "GDP per worker")]


def parse_overrides(sets, switches):
    ov: dict = {}
    for s in sets or []:
        key, val = s.split("=", 1)
        sec, par = key.split(".", 1)
        ov.setdefault(sec, {})[par] = float(val)
    for s in switches or []:
        key, val = s.split("=", 1)
        ov.setdefault("mechanisms", {})[key] = val.lower() in ("on", "true", "1")
    return ov


def save(out: dict, folder: Path, title: str):
    folder.mkdir(parents=True, exist_ok=True)
    with (folder / "paths.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(tm.COLUMNS)
        for i in range(len(out["t"])):
            w.writerow([f"{out[c][i]:.6g}" for c in tm.COLUMNS])
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return
    fig, axes = plt.subplots(2, 2, figsize=(9, 6), sharex=True)
    for ax, (k, lab) in zip(axes.flat, PLOT_VARS):
        ax.plot(out["t"], out[k], color="#2a78d6", lw=2)
        ax.set_title(lab, fontsize=10, loc="left", color="#0b0b0b")
        ax.grid(alpha=0.25, lw=0.6)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
    fig.suptitle(title, fontsize=11, x=0.01, ha="left")
    for ax in axes[1]:
        ax.set_xlabel("year")
    fig.tight_layout()
    fig.savefig(folder / "paths.png", dpi=130)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scenario")
    ap.add_argument("--set", action="append", help="section.param=value")
    ap.add_argument("--switch", action="append", help="mechanism=on|off")
    ap.add_argument("--tag", default="")
    a = ap.parse_args()
    p = tm.load_scenario(a.scenario, parse_overrides(a.set, a.switch))
    out = tm.simulate(p)
    name = Path(a.scenario).stem + (f"__{a.tag}" if a.tag else "")
    folder = Path(__file__).parent / "output" / name
    save(out, folder, f"{name} (trapmodel {tm.MODEL_VERSION})")
    last = {k: round(float(out[k][-1]), 3) for k in ("u", "A", "K", "tau", "GDP", "GNI")}
    print(f"{name}: final {last} -> {folder}")


if __name__ == "__main__":
    main()
