"""Study 9.7, step 0: INEGI's quarterly informal economy by state (MEITEF, base 2018) in tidy form
(D-066).

    python empirics/code/enoe/state_productivity/00_meitef.py            # annual values
    python empirics/code/enoe/state_productivity/00_meitef.py --quarterly

INEGI's 480 tabulados (xlsx), supplied by the user on 2026-11-16, are kept unmodified as one zip
(125 MB, too large to commit) in the uncommitted empirics/data/raw/inegi/. If the zip is missing it is
downloaded from asset ASSET of the (draft) release named RELEASE of wanderdata/devtheory with the GitHub CLI, and its SHA-256
is checked. The tables published "by activity within each state" are read (the tables "by state
within each activity" repeat the same figures), and level measures only are kept: value added at
constant 2018 and current prices, the implicit price index, the volume index, pay (current prices) and
paid jobs. Shares, growth rates and contributions are dropped because they can be derived. The annual
file is committed in empirics/data/source/inegi/meitef_annual.csv.gz as a derived copy of the source.
"""
import argparse
import hashlib
import io
import re
import subprocess
import sys
import zipfile
from pathlib import Path

import openpyxl
import pandas as pd

ROOT = Path(__file__).resolve().parents[4]
RAW = ROOT / "empirics" / "data" / "raw" / "inegi" / "inegi_meitef_base2018_tabulados_2005q1-2026q1.zip"
SHA256 = "d1ef95e826b083f5a769da12c08607511d90296ad642cb3581b0bfff4a636678"
REPO, RELEASE, ASSET = "wanderdata/devtheory", "inegi-meitef", "tabulados_MEITEF.zip"  # draft release, found by name
OUT = ROOT / "empirics" / "data" / "source" / "inegi" / "meitef_annual.csv.gz"
VARIABLE = {"Valor agregado bruto": "gva", "Remuneraciones": "pay", "Puestos de trabajo remunerados": "jobs"}
COMPONENT = {"Economía informal": "informal_economy", "Sector informal": "informal_sector",
             "Otras modalidades de la informalidad": "other_modalities"}
KEEP = {"Millones de pesos anualizados a precios de 2018": "mxn_m_2018",
        "Millones de pesos anualizados a precios corrientes": "mxn_m_current",
        "Índice de precios implícitos base 2018=100": "price_index",
        "Índice de volumen físico, base 2018=100": "volume_index",
        "Unidades": "units"}


def fetch():
    if not RAW.exists():
        RAW.parent.mkdir(parents=True, exist_ok=True)
        rel = subprocess.run(["gh", "api", f"repos/{REPO}/releases", "--jq",
                              f'.[] | select(.name=="{RELEASE}") | .assets[] | select(.name=="{ASSET}") | .id'],
                             capture_output=True, text=True, check=True).stdout.strip().split()[0]
        data = subprocess.run(["gh", "api", "-H", "Accept: application/octet-stream",
                               f"repos/{REPO}/releases/assets/{rel}"], capture_output=True, check=True).stdout
        RAW.write_bytes(data)
    h = hashlib.sha256(RAW.read_bytes()).hexdigest()
    if h != SHA256:
        sys.exit(f"MEITEF zip hash {h} differs from the recorded {SHA256}")


def activity_code(label):
    m = re.match(r"\s*([\d\-]+) - ", label)
    if m:
        return m.group(1)
    l = label.strip().lower()
    return {"actividad económica total": "total", "actividades primarias": "primary",
            "actividades secundarias": "secondary", "actividades terciarias": "tertiary"}.get(l, label.strip())


def parse(raw_bytes, quarterly=False):
    ws = openpyxl.load_workbook(io.BytesIO(raw_bytes), read_only=True)["Tabulado"]
    rows = list(ws.iter_rows(values_only=True))
    path = [p.strip() for p in str(rows[2][0]).split("/")]
    if "por actividad económica" not in path[1]:
        return None
    variable = next(v for k, v in VARIABLE.items() if path[2].startswith(k))
    component = COMPONENT[path[3]]
    state = path[-1]
    years, per = [], []
    y = None
    for a, b in zip(rows[4][1:], rows[5][1:]):
        y = a if a is not None else y
        years.append(int(str(y).rstrip("PR")))
        per.append(str(b).rstrip("PR") if b is not None else None)
    out, measure = [], None
    for r in rows[6:]:
        lab = r[0]
        if lab is None:
            continue
        indent = len(lab) - len(lab.lstrip(" "))
        if indent == 5:
            measure = KEEP.get(lab.strip())
            continue
        if indent < 5:
            break
        if measure is None:
            continue
        for yy, pp, v in zip(years, per, r[1:]):
            if pp is None or pp in ("6 Meses", "9 Meses") or (pp != "Anual" and not quarterly):
                continue
            if v in (None, "", "NA"):
                continue
            out.append((variable, component, state, activity_code(lab), lab.strip(), measure, yy, pp, float(v)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quarterly", action="store_true")
    a = ap.parse_args()
    fetch()
    recs = []
    with zipfile.ZipFile(RAW) as z:
        for n in sorted(z.namelist()):
            if n.endswith(".xlsx"):
                r = parse(z.read(n), a.quarterly)
                if r:
                    recs += r
    d = pd.DataFrame(recs, columns=["variable", "component", "state", "activity", "activity_label", "measure",
                                    "year", "period", "value"])
    d = d.sort_values(["variable", "component", "state", "activity", "measure", "year", "period"])
    if a.quarterly:
        out = RAW.parent / "meitef_quarterly.csv.gz"
        d.to_csv(out, index=False)
    else:
        d = d.drop(columns="period")
        d.to_csv(OUT, index=False, float_format="%.6f", compression={"method": "gzip", "mtime": 0})
        out = OUT
    print(f"{len(d):,} rows, {d['state'].nunique()} geographies, {d['activity'].nunique()} activity codes -> {out}")


if __name__ == "__main__":
    main()
