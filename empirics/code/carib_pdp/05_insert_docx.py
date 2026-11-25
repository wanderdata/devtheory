"""Step 05 (run by hand): insert graphs 1, 2, 4 and 5, the revised text of sections 3.1,
3.2 and 3.4, and annex tables A.1-A.3 into the report, as tracked changes.

    python empirics/code/carib_pdp/05_insert_docx.py DRAFT.docx OUT.docx

The report is not in the repository. Each graph placeholder (a one-column table with a grey
title row, followed by a "Suggested data source" paragraph) is deleted as a tracked change
and replaced by ECLAC-style text paragraphs (label, title, unit; source and notes) around the
figure. Graphs 2, 4 and 5 are inserted as Word charts with an embedded worksheet (drawn from
the same specifications as the Excel workbook); graph 1 as an SVG picture, with the bitmap
fallback that the .docx format requires for versions of Word that cannot read SVG. Remaining
placeholders (graphs 3 and 6-10) get a comment saying what data they need.
All insertions and deletions are attributed to AUTHOR so they can be reviewed in Word.
"""
import copy
import importlib.util
import io
import re
import sys
import zipfile
from pathlib import Path

import pandas as pd
from lxml import etree

from charts import word_chart_parts
from config import DATA, OUTPUT, SECTOR_LABEL, TYPE_SHORT
from specs import build_specs
from texts import figure_texts, report_paragraphs

AUTHOR, DATE = "Claude", "2026-11-25T12:00:00Z"
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
      "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
      "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
      "pic": "http://schemas.openxmlformats.org/drawingml/2006/picture",
      "c": "http://schemas.openxmlformats.org/drawingml/2006/chart",
      "asvg": "http://schemas.microsoft.com/office/drawing/2016/SVG/main",
      "pr": "http://schemas.openxmlformats.org/package/2006/relationships",
      "ct": "http://schemas.openxmlformats.org/package/2006/content-types"}
W = "{%s}" % NS["w"]
EMU_IN = 914400
TEXT_WIDTH_IN = 6.5


def q(tag):
    p, t = tag.split(":")
    return "{%s}%s" % (NS[p], t)


class Ids:
    def __init__(self, start):
        self.n = start

    def __call__(self):
        self.n += 1
        return str(self.n)


def plain(s):
    """The draft uses straight quotes and apostrophes; keep inserted text consistent."""
    return s.replace("’", "'").replace("“", '"').replace("”", '"')


def text_of(e):
    return "".join(t.text or "" for t in e.iter(W + "t"))


# ------------------------------------------------------------------ building tracked content
def mark(tag, ids):
    e = etree.Element(W + tag)
    e.set(W + "id", ids())
    e.set(W + "author", AUTHOR)
    e.set(W + "date", DATE)
    return e


def run(text, bold=False, italic=False, size=None, superscript=False):
    r = etree.Element(W + "r")
    rpr = etree.SubElement(r, W + "rPr")
    if bold:
        etree.SubElement(rpr, W + "b")
    if italic:
        etree.SubElement(rpr, W + "i")
    if size:
        etree.SubElement(rpr, W + "sz").set(W + "val", str(size))
        etree.SubElement(rpr, W + "szCs").set(W + "val", str(size))
    if superscript:
        etree.SubElement(rpr, W + "vertAlign").set(W + "val", "superscript")
    if len(rpr) == 0:
        r.remove(rpr)
    t = etree.SubElement(r, W + "t")
    t.text = plain(text)
    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    return r


def para(runs, ids, ppr=None, align=None, keep_next=False, after=None, before=None, style=None):
    p = etree.Element(W + "p")
    pp = copy.deepcopy(ppr) if ppr is not None else etree.Element(W + "pPr")
    if style:
        etree.SubElement(pp, W + "pStyle").set(W + "val", style)
    if keep_next:
        etree.SubElement(pp, W + "keepNext")
    if after is not None or before is not None:
        sp = etree.SubElement(pp, W + "spacing")
        if before is not None:
            sp.set(W + "before", str(before))
        if after is not None:
            sp.set(W + "after", str(after))
    if align:
        etree.SubElement(pp, W + "jc").set(W + "val", align)
    _order_ppr(pp)
    rpr = pp.find(W + "rPr")
    if rpr is None:
        rpr = etree.SubElement(pp, W + "rPr")
    rpr.insert(0, mark("ins", ids))
    p.append(pp)
    ins = mark("ins", ids)
    for r in runs:
        ins.append(r)
    p.append(ins)
    return p


PPR_ORDER = ["pStyle", "keepNext", "keepLines", "numPr", "spacing", "ind", "jc", "rPr"]


def _order_ppr(pp):
    kids = list(pp)
    kids.sort(key=lambda e: PPR_ORDER.index(etree.QName(e).localname) if etree.QName(e).localname in PPR_ORDER else 50)
    for k in kids:
        pp.remove(k)
    for k in kids:
        pp.append(k)


def delete_runs(container, ids):
    """Wrap every run of a paragraph or table in w:del and mark paragraph marks deleted."""
    for r in list(container.iter(W + "r")):
        if r.getparent().tag == W + "del":
            continue
        for t in r.findall(W + "t"):
            t.tag = W + "delText"
        d = mark("del", ids)
        r.addprevious(d)
        d.append(r)
    for p in container.iter(W + "p"):
        pp = p.find(W + "pPr")
        if pp is None:
            pp = etree.Element(W + "pPr")
            p.insert(0, pp)
        rpr = pp.find(W + "rPr")
        if rpr is None:
            rpr = etree.SubElement(pp, W + "rPr")
        rpr.insert(0, mark("del", ids))


def delete_table(tbl, ids):
    for tr in tbl.findall(W + "tr"):
        trpr = tr.find(W + "trPr")
        if trpr is None:
            trpr = etree.Element(W + "trPr")
            tr.insert(1 if tr.find(W + "tblPrEx") is not None else 0, trpr)
        trpr.append(mark("del", ids))
    delete_runs(tbl, ids)


def tracked_replace(p, old, new, ids):
    """Replace text `old` by `new` inside paragraph p, deleting and inserting only the part that
    differs (common prefix and suffix are kept)."""
    old, new = plain(old), plain(new)
    k = 0
    while k < min(len(old), len(new)) and old[k] == new[k]:
        k += 1
    j = 0
    while j < min(len(old), len(new)) - k and old[-1 - j] == new[-1 - j]:
        j += 1
    # work on whole words: back the common prefix and suffix off to a space, unless the edit
    # is a pure insertion (nothing of the old text is deleted)
    if k + j < len(old):
        while k > 0 and old[k - 1] != " ":
            k -= 1
    if k + j < len(old) and j:
        while j > 0 and old[len(old) - j] not in " .":
            j -= 1
    full = text_of(p)
    start = full.find(old)
    if start < 0:
        raise ValueError(f"text not found: {old[:60]!r}")
    a, b = start + k, start + len(old) - j          # delete [a, b)
    ins_text = new[k:len(new) - j]
    runs = [r for r in p.iter(W + "r") if r.find(W + "t") is not None and r.getparent().tag != W + "del"]
    pos, first_del, last_del, anchor = 0, None, None, None
    for r in runs:
        t = r.find(W + "t")
        s = t.text or ""
        r0, r1 = pos, pos + len(s)
        pos = r1
        if r1 <= a or r0 >= b:
            if r0 >= b and anchor is None and a == b:
                anchor = r
            if r1 == a and a == b and anchor is None:
                anchor = ("after", r)
            continue
        # split run into before / middle / after
        lo, hi = max(a, r0) - r0, min(b, r1) - r0
        if a == b:   # pure insertion inside this run: split it and remember where
            left, right = copy.deepcopy(r), r
            left.find(W + "t").text = s[:lo]
            left.find(W + "t").set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
            right.find(W + "t").text = s[lo:]
            right.find(W + "t").set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
            r.addprevious(left)
            anchor = ("after", left)
            first_del = None
            break
        parts = [(s[:lo], False), (s[lo:hi], True), (s[hi:], False)]
        new_runs = []
        for txt, deleted in parts:
            if not txt:
                continue
            nr = copy.deepcopy(r)
            for extra in nr.findall(W + "t")[1:]:
                nr.remove(extra)
            nt = nr.find(W + "t")
            nt.text = txt
            nt.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
            if deleted:
                nt.tag = W + "delText"
                d = mark("del", ids)
                d.append(nr)
                new_runs.append(d)
                if first_del is None:
                    first_del = d
                last_del = d
            else:
                new_runs.append(nr)
        for nr in new_runs:
            r.addprevious(nr)
        r.getparent().remove(r)
    if ins_text:
        ins = mark("ins", ids)
        template = None
        if first_del is not None:
            template = first_del.find(W + "r")
        rr = run(ins_text)
        if template is not None and template.find(W + "rPr") is not None:
            rr.insert(0, copy.deepcopy(template.find(W + "rPr")))
            for x in rr.findall(W + "rPr")[1:]:
                rr.remove(x)
        ins.append(rr)
        if last_del is not None:
            last_del.addnext(ins)
        elif isinstance(anchor, tuple):
            anchor[1].addnext(ins)
        elif anchor is not None:
            anchor.addprevious(ins)
        else:
            p.append(ins)


# ------------------------------------------------------------------ package helpers
class Package:
    def __init__(self, path):
        self.files = {}
        with zipfile.ZipFile(path) as z:
            for n in z.namelist():
                if not n.endswith("/"):
                    self.files[n] = z.read(n)
        self.doc = etree.fromstring(self.files["word/document.xml"])
        self.rels = etree.fromstring(self.files["word/_rels/document.xml.rels"])
        self.ct = etree.fromstring(self.files["[Content_Types].xml"])
        ids = [int(x) for x in re.findall(rb'wp:docPr id="(\d+)"', self.files["word/document.xml"])]
        self.docpr = max(ids + [0])

    def rel(self, rtype, target, ext=False):
        n = 1 + max(int(r.get("Id")[3:]) for r in self.rels if r.get("Id", "").startswith("rId"))
        r = etree.SubElement(self.rels, q("pr:Relationship"))
        r.set("Id", f"rId{n}")
        r.set("Type", rtype)
        r.set("Target", target)
        return f"rId{n}"

    def default(self, ext, ctype):
        if not any(d.get("Extension") == ext for d in self.ct.findall(q("ct:Default"))):
            d = etree.Element(q("ct:Default"))
            d.set("Extension", ext)
            d.set("ContentType", ctype)
            self.ct.insert(0, d)

    def override(self, part, ctype):
        o = etree.SubElement(self.ct, q("ct:Override"))
        o.set("PartName", part)
        o.set("ContentType", ctype)

    def next_docpr(self):
        self.docpr += 1
        return self.docpr

    def save(self, path):
        self.files["word/document.xml"] = etree.tostring(self.doc, xml_declaration=True, encoding="UTF-8",
                                                         standalone=True)
        self.files["word/_rels/document.xml.rels"] = etree.tostring(self.rels, xml_declaration=True,
                                                                    encoding="UTF-8", standalone=True)
        self.files["[Content_Types].xml"] = etree.tostring(self.ct, xml_declaration=True, encoding="UTF-8",
                                                           standalone=True)
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
            for n, b in self.files.items():
                z.writestr(n, b)


def inline(pkg, cx, cy, name, descr, graphic):
    did = pkg.next_docpr()
    return etree.fromstring(f'''<w:drawing xmlns:w="{NS['w']}" xmlns:wp="{NS['wp']}" xmlns:a="{NS['a']}"><wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="{cx}" cy="{cy}"/><wp:effectExtent l="0" t="0" r="0" b="0"/><wp:docPr id="{did}" name="{name} {did}" descr="{descr}"/><wp:cNvGraphicFramePr/><a:graphic>{graphic}</a:graphic></wp:inline></w:drawing>''')


def add_chart(pkg, spec, n, descr):
    xml, xlsx = word_chart_parts(spec)
    pkg.files[f"word/charts/chart{n}.xml"] = xml
    emb = f"Microsoft_Excel_Worksheet{n}.xlsx"
    pkg.files[f"word/embeddings/{emb}"] = xlsx
    pkg.files[f"word/charts/_rels/chart{n}.xml.rels"] = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        f'<Relationships xmlns="{NS["pr"]}"><Relationship Id="rId1" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/package" '
        f'Target="../embeddings/{emb}"/></Relationships>').encode()
    ext_rid = re.search(rb'<c:externalData r:id="(rId\d+)"', xml)
    if ext_rid and ext_rid.group(1) != b"rId1":
        pkg.files[f"word/charts/chart{n}.xml"] = xml.replace(ext_rid.group(0), b'<c:externalData r:id="rId1"')
    pkg.default("xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    pkg.override(f"/word/charts/chart{n}.xml", "application/vnd.openxmlformats-officedocument.drawingml.chart+xml")
    rid = pkg.rel("http://schemas.openxmlformats.org/officeDocument/2006/relationships/chart", f"charts/chart{n}.xml")
    graphic = (f'<a:graphicData uri="{NS["c"]}"><c:chart xmlns:c="{NS["c"]}" xmlns:r="{NS["r"]}" r:id="{rid}"/>'
               '</a:graphicData>')
    return inline(pkg, int(spec.width_in * EMU_IN), int(spec.height_in * EMU_IN), "Chart", descr, graphic)


def add_svg(pkg, svg_path, png_bytes, n, descr):
    svg = svg_path.read_bytes()
    m = re.search(rb'width="([\d.]+)pt" height="([\d.]+)pt"', svg)
    w_pt, h_pt = float(m.group(1)), float(m.group(2))
    cx = int(TEXT_WIDTH_IN * EMU_IN)
    cy = int(cx * h_pt / w_pt)
    pkg.files[f"word/media/graph{n}.svg"] = svg
    pkg.files[f"word/media/graph{n}_fallback.png"] = png_bytes
    pkg.default("svg", "image/svg+xml")
    pkg.default("png", "image/png")
    img = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image"
    r_png = pkg.rel(img, f"media/graph{n}_fallback.png")
    r_svg = pkg.rel(img, f"media/graph{n}.svg")
    graphic = (f'<a:graphicData uri="{NS["pic"]}"><pic:pic xmlns:pic="{NS["pic"]}" xmlns:r="{NS["r"]}">'
               f'<pic:nvPicPr><pic:cNvPr id="0" name="graph{n}.svg" descr="{descr}"/><pic:cNvPicPr/></pic:nvPicPr>'
               f'<pic:blipFill><a:blip r:embed="{r_png}"><a:extLst><a:ext uri="{{96DAC541-7B7A-43D3-8B79-37D633B846F1}}">'
               f'<asvg:svgBlip xmlns:asvg="{NS["asvg"]}" r:embed="{r_svg}"/></a:ext></a:extLst></a:blip>'
               '<a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
               f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
               '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData>')
    return inline(pkg, cx, cy, "Picture", descr, graphic)


def fallback_png():
    """Bitmap fallback for graph 1, drawn by step 02's own function (not a deliverable)."""
    spec = importlib.util.spec_from_file_location("svgfig", Path(__file__).with_name("02_svg_figures.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    g1 = pd.read_csv(DATA / "g1_decomposition.csv", keep_default_na=False, na_values=[""])
    g1["grade"] = g1["grade"].fillna("")
    fig = mod.graph1(g1)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=200)
    return buf.getvalue()


# ------------------------------------------------------------------ ECLAC blocks
def heading_block(t, ids, panel_lines=None):
    out = [para([run(t["label"], bold=True)], ids, align="center", keep_next=True, after=0),
           para([run(t["title"], bold=True)], ids, align="center", keep_next=True, after=0)]
    if t.get("unit"):
        out.append(para([run(t["unit"])], ids, align="center", keep_next=True, after=120))
    return out


def panel_heading(text, ids):
    title, unit = text.split("\n")
    return [para([run(title, bold=True, size=20)], ids, align="center", keep_next=True, before=120, after=0),
            para([run(unit, size=20)], ids, align="center", keep_next=True, after=60)]


def figure_para(drawing, ids):
    r = etree.Element(W + "r")
    r.append(drawing)
    return para([r], ids, align="center", keep_next=True, after=60)


def notes_block(t, ids):
    out = [para([run("Source: ", italic=True, size=18), run(t["source"], size=18)], ids, after=0, align="both")]
    for tag, text in t["notes"]:
        if tag == "Note":
            rr = [run("Note: ", italic=True, size=18), run(text, size=18)]
        else:
            rr = [run(tag, size=18, superscript=True), run(" " + text, size=18)]
        out.append(para(rr, ids, after=0, align="both"))
    out[-1] = _space_after(out[-1], 240)
    return out


def _space_after(p, v):
    pp = p.find(W + "pPr")
    sp = pp.find(W + "spacing")
    if sp is None:
        sp = etree.SubElement(pp, W + "spacing")
    sp.set(W + "after", str(v))
    _order_ppr(pp)
    return p


def word_table(df, ids, numfmt, first_cols=1, size=16):
    """ECLAC-style table: rules above and below the header and at the bottom, no vertical lines."""
    ncol = len(df.columns)
    total = int(TEXT_WIDTH_IN * 1440)
    first_w = 2200 if first_cols == 1 else 1500
    widths = [first_w] * first_cols + [int((total - first_w * first_cols) / (ncol - first_cols))] * (ncol - first_cols)
    tbl = etree.Element(W + "tbl")
    tp = etree.SubElement(tbl, W + "tblPr")
    etree.SubElement(tp, W + "tblW").attrib.update({W + "w": str(sum(widths)), W + "type": "dxa"})
    b = etree.SubElement(tp, W + "tblBorders")
    for side in ("top", "bottom"):
        etree.SubElement(b, W + side).attrib.update({W + "val": "single", W + "sz": "6", W + "space": "0",
                                                      W + "color": "auto"})
    etree.SubElement(tp, W + "tblLayout").set(W + "type", "fixed")
    cm = etree.SubElement(tp, W + "tblCellMar")
    for side in ("left", "right"):
        etree.SubElement(cm, W + side).attrib.update({W + "w": "57", W + "type": "dxa"})
    grid = etree.SubElement(tbl, W + "tblGrid")
    for w_ in widths:
        etree.SubElement(grid, W + "gridCol").set(W + "w", str(w_))

    def row(values, header=False):
        tr = etree.SubElement(tbl, W + "tr")
        trpr = etree.SubElement(tr, W + "trPr")
        if header:
            etree.SubElement(trpr, W + "tblHeader")
        trpr.append(mark("ins", ids))
        for j, v in enumerate(values):
            tc = etree.SubElement(tr, W + "tc")
            tcp = etree.SubElement(tc, W + "tcPr")
            etree.SubElement(tcp, W + "tcW").attrib.update({W + "w": str(widths[j]), W + "type": "dxa"})
            if header:
                tb = etree.SubElement(tcp, W + "tcBorders")
                etree.SubElement(tb, W + "bottom").attrib.update({W + "val": "single", W + "sz": "4",
                                                                  W + "space": "0", W + "color": "auto"})
            etree.SubElement(tcp, W + "vAlign").set(W + "val", "bottom")
            if isinstance(v, (int, float)) and not pd.isna(v):
                txt = format(v, numfmt)
                txt = txt.lstrip("-") if float(txt) == 0 else txt.replace("-", "−")
                align = "right"
            else:
                txt = "" if (v is None or (isinstance(v, float) and pd.isna(v))) else str(v)
                align = "left" if j < first_cols else ("center" if header else "right")
            tc.append(para([run(txt, bold=header, size=size)], ids, after=0, align=align))
    row(list(df.columns), header=True)
    for rec in df.itertuples(index=False):
        row(list(rec))
    return tbl


# ------------------------------------------------------------------ comments
def add_comment(pkg, p, text, ids):
    cid = ids()
    cpath = "word/comments.xml"
    if cpath not in pkg.files:
        pkg.files[cpath] = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                            f'<w:comments xmlns:w="{NS["w"]}"/>').encode()
        pkg.override("/word/comments.xml",
                     "application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml")
        pkg.rel("http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments", "comments.xml")
    root = etree.fromstring(pkg.files[cpath])
    c = etree.SubElement(root, W + "comment")
    c.attrib.update({W + "id": cid, W + "author": AUTHOR, W + "date": DATE, W + "initials": "C"})
    cp = etree.SubElement(c, W + "p")
    cr = etree.SubElement(cp, W + "r")
    t = etree.SubElement(cr, W + "t")
    t.text = text
    pkg.files[cpath] = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)
    start = etree.Element(W + "commentRangeStart")
    start.set(W + "id", cid)
    end = etree.Element(W + "commentRangeEnd")
    end.set(W + "id", cid)
    ref_r = etree.Element(W + "r")
    etree.SubElement(ref_r, W + "commentReference").set(W + "id", cid)
    first = p.find(W + "pPr")
    if first is not None:
        first.addnext(start)
    else:
        p.insert(0, start)
    p.append(end)
    p.append(ref_r)


# ------------------------------------------------------------------ main
def find_placeholder(body, label):
    for e in body:
        if e.tag == W + "tbl" and text_of(e).strip().startswith(label + ":"):
            nxt = e.getnext()
            src = nxt if nxt is not None and text_of(nxt).startswith("Suggested data source") else None
            return e, src
    raise ValueError(f"placeholder for {label} not found")


def find_para(body, start):
    for e in body:
        if e.tag == W + "p" and text_of(e).startswith(start):
            return e
    raise ValueError(f"paragraph starting {start!r} not found")


def replace_placeholder(body, label, block, ids):
    tbl, src = find_placeholder(body, label)
    for e in block:
        tbl.addprevious(e)
    delete_table(tbl, ids)
    if src is not None:
        delete_runs(src, ids)
    return src if src is not None else tbl


def main(src, dst):
    pkg = Package(src)
    body = pkg.doc.find(W + "body")
    ids = Ids(9000)
    T = figure_texts()
    P = report_paragraphs()
    specs = build_specs()

    # 3.1: fourth group, after the "Mixed economies" bullet (same list formatting)
    mixed = find_para(body, "Mixed economies:")
    bullet_ppr = copy.deepcopy(mixed.find(W + "pPr"))
    for x in bullet_ppr.findall(W + "rPr"):
        bullet_ppr.remove(x)
    lead, rest = P["3.1_other"].split(":", 1)
    mixed.addnext(para([run(lead + ":", bold=True), run(rest)], ids, ppr=bullet_ppr))

    # 3.2: lead-in sentence
    p32 = find_para(body, "Labour productivity grows through two channels")
    tracked_replace(p32, "ECLAC's published decomposition covers the region as a whole, and a Caribbean version "
                         "disaggregated by production type remains to be produced.", P["3.2_lead"], ids)

    # Graph 1
    svg = OUTPUT / "figures" / "graph1_decomposition.svg"
    g1 = (heading_block(T["graph1"], ids)
          + [figure_para(add_svg(pkg, svg, fallback_png(), 1, plain(T["graph1"]["title"])), ids)]
          + notes_block(T["graph1"], ids))
    replace_placeholder(body, "Graph 1", g1, ids)

    # Graph 2 (two Word charts), then the new text of 3.2
    g2 = heading_block(T["graph2"], ids)
    for n, key in ((1, "graph2a"), (2, "graph2b")):
        g2 += panel_heading(T["graph2"]["panels"][key], ids)
        g2.append(figure_para(add_chart(pkg, specs[key], n, plain(T["graph2"]["panels"][key].replace("\n", " "))), ids))
    g2 += notes_block(T["graph2"], ids)
    last = replace_placeholder(body, "Graph 2", g2, ids)
    for text in reversed(P["3.2_after"]):
        last.addnext(para([run(text)], ids))

    # 3.4: replace the illustrative example
    p34 = find_para(body, "In an economy with a labour force of 100,000")
    tracked_replace(p34, "In an economy with a labour force of 100,000, a cluster or firm employing 5,000 workers "
                         "accounts for five percent of employment (illustrative figures).", P["3.4"], ids)

    # Graphs 4 and 5 (Word charts) and in-text references
    for n, key in ((3, "graph4"), (4, "graph5")):
        blk = (heading_block(T[key], ids)
               + [figure_para(add_chart(pkg, specs[key], n, plain(T[key]["title"])), ids)]
               + notes_block(T[key], ids))
        replace_placeholder(body, T[key]["label"], blk, ids)
    tracked_replace(find_para(body, "ECLAC treats cluster initiatives"), "against 367 in Brazil.",
                    "against 367 in Brazil (graph 4).", ids)
    tracked_replace(find_para(body, "ECLAC's data indicate a thin STI"), "and 109 in Brazil.",
                    "and 109 in Brazil (graph 5).", ids)

    # Comments on the placeholders still to be filled
    needs = {"Graph 3": "Needs IMF World Economic Outlook (gross debt, interest, revenue) for Caribbean States; "
                        "not in hand.",
             "Graph 6": "Needs international tourism receipts (World Bank WDI or UN Tourism) and tourism "
                        "employment (WTTC or UN Tourism); not in hand.",
             "Graph 7": "Needs commercial electricity tariffs by country (CDB or CARILEC); not in hand.",
             "Graph 8": "Needs emigration rates of the highly skilled (Mishra 2006, table 1, or OECD DIOC) and "
                        "remittances as a share of GDP (World Bank WDI); not in hand.",
             "Graph 9": "Output of the proposed DRIL mapping; no data yet.",
             "Graph 10": "Output of the proposed DRIL mapping (with GTED tax expenditures and IMF interest "
                         "payments); no data yet."}
    for label, text in needs.items():
        tbl, _ = find_placeholder(body, label)
        add_comment(pkg, tbl.find(f".//{W}tr").find(f".//{W}p"), text, ids)

    # Annex after the references
    sect = body.find(W + "sectPr")
    add = []
    add.append(para([run("Annex")], ids, style="Heading1"))
    tables = annex_tables()
    for key, (df, fmt, first) in tables.items():
        add += heading_block(T[key], ids)
        add.append(word_table(df, ids, fmt, first_cols=first))
        add += notes_block(T[key], ids)
    for e in add:
        sect.addprevious(e)
    pkg.save(dst)
    print("written", dst)


def annex_tables():
    g = pd.read_csv(DATA / "g1_decomposition.csv", keep_default_na=False, na_values=[""])
    g["grade"] = g["grade"].fillna("")
    w = g.pivot_table(index=["period", "type", "unit", "name", "grade"], columns="base",
                      values=["growth_pp", "within_pp", "struct_pp"], aggfunc="first")
    w.columns = [f"{a}_{b}" for a, b in w.columns]
    w = w.reset_index()
    from config import TYPES
    w["o1"] = w["type"].map({t: i for i, t in enumerate(TYPES)})
    w["o2"] = (w["unit"] == "country").astype(int)
    w = w.sort_values(["period", "o1", "o2", "name"])
    a1 = pd.DataFrame({
        "Period and economy": [f"{TYPE_SHORT[t]}, pooled" if u == "type" else n
                               for t, u, n in zip(w["type"], w["unit"], w["name"])],
        "Period": w["period"].values,
        "Grade": w["grade"].replace({"pooled": "–"}).values,
        "Growth": w["growth_pp_chained"].values, "Within sectors": w["within_pp_chained"].values,
        "Structural, chained": w["struct_pp_chained"].values,
        "Structural, initial-year prices": w["struct_pp_initial"].values,
        "Structural, final-year prices": w["struct_pp_final"].values})
    # one table, with the period as a spanning text row
    rows = []
    for per, d in a1.groupby("Period", sort=True):
        rows.append({"Period and economy": per})
        rows += d.drop(columns="Period").to_dict("records")
    a1 = pd.DataFrame(rows, columns=[c for c in a1.columns if c != "Period"])
    a1["Grade"] = a1["Grade"].fillna("")

    a = pd.read_csv(DATA / "a2_sectors_countries.csv")
    sh = "\u00ad"   # soft hyphen: lets Word break long headers cleanly
    short = {"AGR": f"Agri{sh}culture", "MIU": "Mining and utilities", "MAN": f"Manu{sh}facturing",
             "CON": f"Con{sh}struction",
             "TRH": "Trade, restaurants and hotels", "TSC": "Transport and comms.", "OTH": "Other services"}
    def wide(value, drop_cuba):
        x = a[a["iso3"] != "CUB"] if drop_cuba else a
        order = x.drop_duplicates("iso3")["name"].tolist()
        p = x.pivot(index="name", columns="sector", values=value).loc[order, list(short)]
        p.columns = [short[c] for c in p.columns]
        return p.reset_index().rename(columns={"name": "Economy"})
    return {"tableA1": (a1, ".2f", 1), "tableA2": (wide("emp_share_pct", False), ".1f", 1),
            "tableA3": (wide("rel_lp", True), ".2f", 1)}


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    main(Path(sys.argv[1]), Path(sys.argv[2]))
