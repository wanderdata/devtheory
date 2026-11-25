"""Step 03: Excel workbook with the data and native charts of the report's graphs.

    empirics/output/carib_pdp/caribbean_pdp_graphs.xlsx

One sheet per graph or annex table: label, title and unit (ECLAC style) at the top, the data
plotted, the source and notes, and the chart beside the data for graphs 2, 4 and 5. Graph 1
is an SVG (figures/graph1_decomposition.svg); its sheet holds the plotted values.
The file is written with fixed document properties so that a rebuild is byte-identical.
"""
from datetime import datetime

import pandas as pd
import xlsxwriter

from charts import add_to_workbook
from config import DATA, OUTPUT, SECTOR_LABEL, SECTORS, TYPE_SHORT
from specs import build_specs
from texts import box_texts, figure_texts

FONT = "Calibri"


def header(wb, ws, t, panel=None):
    f_label = wb.add_format({"bold": True, "font_name": FONT, "font_size": 10})
    f_title = wb.add_format({"bold": True, "font_name": FONT, "font_size": 10})
    f_unit = wb.add_format({"italic": False, "font_name": FONT, "font_size": 9})
    ws.write(0, 0, t["label"], f_label)
    ws.write(1, 0, t["title"], f_title)
    ws.write(2, 0, t["unit"] or "", f_unit)
    return 4


def footer(wb, ws, t, row):
    f = wb.add_format({"font_name": FONT, "font_size": 8, "text_wrap": False})
    ws.write(row, 0, "Source: " + t["source"], f)
    row += 1
    for tag, text in t["notes"]:
        ws.write(row, 0, (f"{tag}: " if tag == "Note" else f"{tag} ") + text, f)
        row += 1
    return row


def table(wb, ws, df, row, numfmt):
    head = wb.add_format({"bold": True, "font_name": FONT, "font_size": 9, "bottom": 1, "text_wrap": True,
                          "valign": "bottom"})
    body = wb.add_format({"font_name": FONT, "font_size": 9})
    num = wb.add_format({"font_name": FONT, "font_size": 9, "num_format": numfmt})
    for j, c in enumerate(df.columns):
        ws.write(row, j, c, head)
    for i, rec in enumerate(df.itertuples(index=False), start=1):
        for j, v in enumerate(rec):
            if isinstance(v, (int, float)) and not pd.isna(v):
                ws.write_number(row + i, j, float(v), num)
            else:
                ws.write(row + i, j, "" if pd.isna(v) else v, body)
    return row + len(df) + 2


def g1_table():
    g = pd.read_csv(DATA / "g1_decomposition.csv", keep_default_na=False, na_values=[""])
    g["grade"] = g["grade"].fillna("")
    w = g.pivot_table(index=["period", "type", "unit", "name", "grade"], columns="base",
                      values=["growth_pp", "within_pp", "struct_pp"], aggfunc="first")
    w.columns = [f"{a}_{b}" for a, b in w.columns]
    w = w.reset_index()
    from config import TYPES
    order = {t: i for i, t in enumerate(TYPES)}
    w["o1"] = w["type"].map(order)
    w["o2"] = (w["unit"] == "country").astype(int)
    w = w.sort_values(["period", "o1", "o2", "name"])
    w["Economy"] = w.apply(lambda r: f"{TYPE_SHORT[r['type']]} (pooled)" if r["unit"] == "type" else r["name"], axis=1)
    out = pd.DataFrame({
        "Period": w["period"], "Production type": w["type"].map(TYPE_SHORT), "Economy": w["Economy"],
        "Data grade": w["grade"].replace({"pooled": "—"}),
        "Growth (chained)": w["growth_pp_chained"], "Within sectors (chained)": w["within_pp_chained"],
        "Structural change (chained)": w["struct_pp_chained"],
        "Structural change (initial-year prices)": w["struct_pp_initial"],
        "Structural change (final-year prices)": w["struct_pp_final"]})
    return out.reset_index(drop=True)


def sector_wide(value, drop_cuba=False):
    a = pd.read_csv(DATA / "a2_sectors_countries.csv")
    if drop_cuba:
        a = a[a["iso3"] != "CUB"]
    order = a.drop_duplicates("iso3")[["iso3", "name", "type"]]
    w = a.pivot(index="iso3", columns="sector", values=value)[SECTORS]
    w.columns = [SECTOR_LABEL[c] for c in w.columns]
    w = order.set_index("iso3").join(w).reset_index(drop=True)
    w["type"] = w["type"].map(TYPE_SHORT)
    return w.rename(columns={"name": "Economy", "type": "Production type"})[
        ["Production type", "Economy"] + [SECTOR_LABEL[c] for c in SECTORS]]


def main():
    texts = figure_texts()
    specs = build_specs()
    path = OUTPUT / "caribbean_pdp_graphs.xlsx"
    wb = xlsxwriter.Workbook(path)
    wb.set_properties({"title": "Productive Development Policy in the Caribbean: data for graphs and annex tables",
                       "author": "Paul Wander", "created": datetime(2026, 11, 25)})
    note = wb.add_format({"font_name": FONT, "font_size": 9, "italic": True})

    ws = wb.add_worksheet("Contents")
    rows = [("Graph 1", "SVG figure (figures/graph1_decomposition.svg); data in sheet 'Graph 1'"),
            ("Graph 2", "Excel charts, panels A and B"), ("Graph 4", "Excel chart"), ("Graph 5", "Excel chart"),
            ("Box 1", "Excel chart (Graph B1) and supporting data"), ("Table A.1", "Annex"), ("Table A.2", "Annex"), ("Table A.3", "Annex"),
            ("Section 3.4", "Total employment by country, 2024")]
    ws.write(0, 0, "Productive Development Policy in the Caribbean: data for graphs and annex tables",
             wb.add_format({"bold": True, "font_name": FONT, "font_size": 11}))
    for i, (a, b) in enumerate(rows, start=2):
        ws.write(i, 0, a)
        ws.write(i, 1, b)
    ws.write(len(rows) + 3, 0, "Generated by empirics/code/carib_pdp (repository wanderdata/devtheory). "
             "Graphs 3 and 6–10 need data not yet in hand.", note)
    ws.set_column(0, 0, 14)
    ws.set_column(1, 1, 70)

    ws = wb.add_worksheet("Graph 1")
    r = header(wb, ws, texts["graph1"])
    ws.write(r, 0, "The figure is supplied as an SVG file (figures/graph1_decomposition.svg).", note)
    r = table(wb, ws, g1_table(), r + 2, "0.00")
    footer(wb, ws, texts["graph1"], r)
    ws.set_column(0, 2, 22)
    ws.set_column(3, 8, 14)

    ws = wb.add_worksheet("Graph 2")
    r = header(wb, ws, texts["graph2"])
    for k, key in enumerate(["graph2a", "graph2b"]):
        ws.write(r, 0, texts["graph2"]["panels"][key].replace("\n", " "),
                 wb.add_format({"bold": True, "font_name": FONT, "font_size": 9}))
        add_to_workbook(wb, ws, specs[key], r + 1, 0, f"G{r + 2}")
        r += 20
    footer(wb, ws, texts["graph2"], r)
    ws.set_column(0, 0, 30)
    ws.set_column(1, 4, 19)

    for key in ("graph4", "graph5"):
        ws = wb.add_worksheet(texts[key]["label"])
        r = header(wb, ws, texts[key])
        end = add_to_workbook(wb, ws, specs[key], r, 0, f"D{r + 1}")
        footer(wb, ws, texts[key], r + len(specs[key].categories) + 14)
        ws.set_column(0, 0, 32)
        ws.set_column(1, 1, 12)

    bt = box_texts()
    ws = wb.add_worksheet("Box 1")
    gb = dict(bt["graph"])
    r = header(wb, ws, gb)
    end = add_to_workbook(wb, ws, specs["box1"], r, 0, f"E{r + 1}")
    r += len(specs["box1"].categories) + 18
    b1 = pd.read_csv(DATA / "box1_sectors.csv")
    b1 = b1.pivot_table(index=["period", "sector"], columns="base", values=["within_pp", "struct_pp"]).reset_index()
    b1.columns = [f"{a} ({b})" if b else a for a, b in b1.columns]
    b1["sector"] = b1["sector"].map(SECTOR_LABEL)
    ws.write(r, 0, "All price bases (percentage points per year)", wb.add_format({"bold": True, "font_name": FONT}))
    r = table(wb, ws, b1, r + 1, "0.00")
    rp = pd.read_csv(DATA / "box1_relprices.csv")
    rp = pd.DataFrame({"Economy": rp["country"], "Sector": rp["sector"].map(SECTOR_LABEL),
                       "Change in relative productivity, current prices": rp["d_nom_pp"],
                       "of which real (constant prices)": rp["d_real_pp"],
                       "of which relative price": rp["d_price_pp"]})
    ws.write(r, 0, "Change in productivity relative to the economy-wide average, 2000–2019 (log points per year)",
             wb.add_format({"bold": True, "font_name": FONT}))
    r = table(wb, ws, rp, r + 1, "0.00")
    footer(wb, ws, gb, r)
    ws.set_column(0, 1, 30)
    ws.set_column(2, 7, 16)

    for key, df, fmt in [("tableA1", g1_table(), "0.00"),
                         ("tableA2", sector_wide("emp_share_pct"), "0.0"),
                         ("tableA3", sector_wide("rel_lp", drop_cuba=True), "0.00")]:
        ws = wb.add_worksheet(texts[key]["label"])
        r = header(wb, ws, texts[key])
        r = table(wb, ws, df, r, fmt)
        footer(wb, ws, texts[key], r)
        ws.set_column(0, 1, 24)
        ws.set_column(2, 9, 14)

    ws = wb.add_worksheet("Section 3.4")
    ws.write(0, 0, "Caribbean (12 countries): total employment, 2024", wb.add_format({"bold": True, "font_name": FONT}))
    ws.write(1, 0, "(Thousands of people)")
    e = pd.read_csv(DATA / "s34_employment.csv")
    e = pd.DataFrame({"Economy": e["name"], "Production type": e["type"].map(TYPE_SHORT),
                      "Employment (thousands)": e["employment_thousands"]})
    r = table(wb, ws, e, 3, "#,##0")
    ws.write(r, 0, "Source: Prepared by the author, on the basis of International Labour Organization (ILO), ILOSTAT "
             "database (ILO modelled estimates).")
    ws.set_column(0, 2, 26)
    wb.close()
    print("workbook written:", path)


if __name__ == "__main__":
    main()
