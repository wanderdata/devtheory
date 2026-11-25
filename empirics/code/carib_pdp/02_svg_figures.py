"""Step 02: SVG figures for graphs that Excel cannot draw clearly (Graph 1).

Graph 1: within-sector and structural change terms of labour productivity growth
(percentage points per year, chained previous-year prices) by country and pooled by
production type, 2000-2019 and 2019-2024. Bars for grade C country-periods (both period
ends more than two years from a usable survey year) are drawn pale; a 'b' marks rows whose
structural term changes sign across the three price bases; values beyond the axis are cut
and printed ('a'). Titles, units, sources and notes are text in the report, not in the SVG.

Text is kept as SVG text in Calibri (Carlito, metric-compatible, is used for layout), so
the figure can be edited in Word or a vector editor.
"""
import re

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

from config import DATA, OUTPUT, PERIODS, TYPES, TYPE_SHORT  # noqa: E402

BASE = "chained"
XLIM = (-6, 8)
ZLIM = (-1, 1)
WITHIN, STRUCT, INK, MUTED, GRID = "#257de0", "#f47230", "#191919", "#666666", "#d9d9d9"
plt.rcParams.update({"font.family": ["Carlito", "DejaVu Sans"], "font.size": 8.5, "svg.fonttype": "none",
                     "svg.hashsalt": "carib_pdp", "axes.linewidth": 0.6})


def rows(g1):
    """Row order: for each type, a header, the pooled row, then countries by name."""
    out = []
    for t in TYPES:
        out.append(("header", t, TYPE_SHORT[t] + " economies" if not t.startswith("Other") else t))
        if ((g1["unit"] == "type") & (g1["name"] == t)).any():
            out.append(("type", t, "Pooled"))
        for name in sorted(g1.loc[(g1["unit"] == "country") & (g1["type"] == t), "name"].unique()):
            out.append(("country", name, name))
    return out


def _bar(ax, y, w, s, alpha, show_within=True):
    s_left = w if (show_within and (w >= 0) == (s >= 0)) else 0.0
    h = 0.62
    if show_within:
        ax.barh(y, w, height=h, color=WITHIN, alpha=alpha, edgecolor="white", lw=0.6, zorder=2)
    ax.barh(y, s, left=s_left, height=h, color=STRUCT, alpha=alpha, edgecolor="white", lw=0.6, zorder=2)
    return s_left


def _frame(ax, lim, step, n):
    ax.axvline(0, color=INK, lw=0.6, zorder=1)
    ticks = [round(lim[0] + i * step, 6) for i in range(int(round((lim[1] - lim[0]) / step)) + 1)]
    for x in ticks:
        if x:
            ax.axvline(x, color=GRID, lw=0.4, zorder=0)
    ax.set_xlim(*lim)
    ax.set_ylim(-0.7, n - 0.3)
    ax.set_xticks(ticks)
    ax.set_xticklabels([f"{x:g}".replace("-", "−") for x in ticks])
    ax.tick_params(axis="both", length=0, labelsize=7.5, colors=INK)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(MUTED)


def graph1(g1):
    g = g1[g1["base"] == BASE]
    layout = rows(g1)
    n = len(layout)
    height = 0.23 * n + 1.15
    fig, axes = plt.subplots(1, 4, figsize=(6.5, height), sharey=True,
                             gridspec_kw={"wspace": 0.12, "width_ratios": [3, 2, 3, 2]})
    ys = list(range(n))[::-1]
    for k, (t0, T) in enumerate(PERIODS):
        per = f"{t0}–{T}"
        ax, az = axes[2 * k], axes[2 * k + 1]
        _frame(ax, XLIM, 2, n)
        _frame(az, ZLIM, 0.5, n)
        for y, (kind, key, _) in zip(ys, layout):
            if kind == "header":
                continue
            unit = "type" if kind == "type" else "country"
            r = g[(g["unit"] == unit) & (g["name"] == key) & (g["period"] == per)]
            if r.empty:
                continue
            r = r.iloc[0]
            w, s, tot = r["within_pp"], r["struct_pp"], r["growth_pp"]
            alpha = 0.35 if r["grade"] == "C" else 1.0
            s_left = _bar(ax, y, w, s, alpha)
            if tot > XLIM[1] or max(w, s_left + s) > XLIM[1]:
                ax.text(XLIM[1] - 0.15, y, f"{tot:.1f}ᵃ", ha="right", va="center", fontsize=7, color="white",
                        fontweight="bold", zorder=4)
            else:
                ax.plot([tot], [y], marker="D", ms=3.4, color=INK, mec="white", mew=0.6, zorder=3)
            _bar(az, y, w, s, alpha, show_within=False)
            if s > ZLIM[1] or s < ZLIM[0]:
                xe = ZLIM[1] - 0.05 if s > 0 else ZLIM[0] + 0.05
                az.text(xe, y, f"{s:.1f}ᵃ".replace("-", "−"), ha="right" if s > 0 else "left", va="center",
                        fontsize=7, color="white", fontweight="bold", zorder=4)
            if r["agreement"] == "sign depends on price base":
                az.text(ZLIM[1] - 0.04, y, "b", ha="right", va="center", fontsize=7.5, color=INK, fontweight="bold")
        ax.set_title("Decomposition", fontsize=7.5, color=MUTED, pad=3)
        az.set_title("Structural change", fontsize=7.5, color=MUTED, pad=3)
        x0 = ax.get_position().x0
        x1 = az.get_position().x1
    axes[0].set_yticks(ys)
    labels = axes[0].set_yticklabels([lab for _, _, lab in layout])
    for lab, (kind, _, _) in zip(labels, layout):
        if kind == "header":
            lab.set_fontweight("bold")
        elif kind == "type":
            lab.set_fontstyle("italic")
    top = 1 - 0.78 / height
    fig.subplots_adjust(left=0.27, right=0.975, top=top, bottom=0.55 / height)
    for k, (t0, T) in enumerate(PERIODS):
        x0 = axes[2 * k].get_position().x0
        x1 = axes[2 * k + 1].get_position().x1
        yt = top + 0.24 / height
        fig.text((x0 + x1) / 2, yt, f"{t0}–{T}", ha="center", va="bottom", fontsize=9, fontweight="bold",
                 color=INK)
        fig.add_artist(plt.Line2D([x0, x1], [yt - 0.02 / height, yt - 0.02 / height], color=MUTED, lw=0.6))
    fig.supxlabel("Percentage points per year", fontsize=8, color=MUTED, y=0.035)
    handles = [plt.Rectangle((0, 0), 1, 1, color=WITHIN), plt.Rectangle((0, 0), 1, 1, color=STRUCT),
               plt.Line2D([], [], marker="D", ms=4, color=INK, lw=0),
               plt.Rectangle((0, 0), 1, 1, color=WITHIN, alpha=0.35)]
    fig.legend(handles, ["Within sectors", "Structural change", "Total growth",
                         "Modelled employment only (pale)"],
               loc="upper center", ncol=4, frameon=False, fontsize=8, bbox_to_anchor=(0.6, 1.0),
               handlelength=1.2, columnspacing=1.2)
    return fig


def save_svg(fig, path):
    fig.savefig(path, format="svg", metadata={"Date": None, "Creator": None})
    plt.close(fig)
    s = path.read_text(encoding="utf8")
    s = re.sub(r"font-family:\s*'?Carlito'?", "font-family: 'Calibri', 'Carlito', sans-serif", s)
    s = s.replace("font: ", "font-family: 'Calibri', 'Carlito', sans-serif; font: ") if "font-family" not in s else s
    path.write_text(s, encoding="utf8")


def main():
    g1 = pd.read_csv(DATA / "g1_decomposition.csv", keep_default_na=False, na_values=[""])
    g1["grade"] = g1["grade"].fillna("")
    (OUTPUT / "figures").mkdir(parents=True, exist_ok=True)
    save_svg(graph1(g1), OUTPUT / "figures" / "graph1_decomposition.svg")
    print("SVG figures written")


if __name__ == "__main__":
    main()
