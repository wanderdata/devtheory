"""Step 06 (run by hand): Box 1 on labour productivity in the tourism and services economies,
as a separate Word document in the report's own styles (D-073).

    python empirics/code/carib_pdp/06_box_docx.py DRAFT.docx OUT.docx

The report is used only as a template: its body is emptied and the box is written in its
place, untracked, as a shaded one-cell table holding the title, text, Graph B1 (a Word chart
with an embedded worksheet) and its source and note, ready to paste into section 3.3.
"""
import importlib.util
import sys
from pathlib import Path

from lxml import etree

from specs import build_specs
from texts import box_texts

spec = importlib.util.spec_from_file_location("insert", Path(__file__).with_name("05_insert_docx.py"))
ins = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ins)
ins.TRACK = False
W = ins.W


def box_table(content, width):
    tbl = etree.Element(W + "tbl")
    tp = etree.SubElement(tbl, W + "tblPr")
    etree.SubElement(tp, W + "tblW").attrib.update({W + "w": str(width), W + "type": "dxa"})
    b = etree.SubElement(tp, W + "tblBorders")
    for side in ("top", "left", "bottom", "right"):
        etree.SubElement(b, W + side).attrib.update({W + "val": "single", W + "sz": "4", W + "space": "0",
                                                      W + "color": "808080"})
    etree.SubElement(tp, W + "tblLayout").set(W + "type", "fixed")
    cm = etree.SubElement(tp, W + "tblCellMar")
    for side, v in (("top", 113), ("left", 170), ("bottom", 113), ("right", 170)):
        etree.SubElement(cm, W + side).attrib.update({W + "w": str(v), W + "type": "dxa"})
    etree.SubElement(etree.SubElement(tbl, W + "tblGrid"), W + "gridCol").set(W + "w", str(width))
    tr = etree.SubElement(tbl, W + "tr")
    tc = etree.SubElement(tr, W + "tc")
    tcp = etree.SubElement(tc, W + "tcPr")
    etree.SubElement(tcp, W + "tcW").attrib.update({W + "w": str(width), W + "type": "dxa"})
    etree.SubElement(tcp, W + "shd").attrib.update({W + "val": "clear", W + "color": "auto", W + "fill": "F2F2F2"})
    for e in content:
        tc.append(e)
    return tbl


def main(src, dst):
    pkg = ins.Package(src)
    body = pkg.doc.find(W + "body")
    for e in list(body):
        if e.tag != W + "sectPr":
            body.remove(e)
    # drop relationships to parts the emptied body no longer uses (the report's figure)
    for r in list(pkg.rels):
        if r.get("Type").endswith("/image"):
            pkg.files.pop("word/" + r.get("Target"), None)
            pkg.rels.remove(r)
    ids = ins.Ids(0)
    t = box_texts()
    g = t["graph"]
    content = [ins.para([ins.run(t["label"], bold=True)], ids, align="center", keep_next=True, after=0),
               ins.para([ins.run(t["title"], bold=True)], ids, align="center", keep_next=True, after=160)]
    for text in t["paragraphs"][:2]:
        content.append(ins.para([ins.run(text)], ids, align="both"))
    content += ins.heading_block(g, ids)
    sp = build_specs()["box1"]
    content.append(ins.figure_para(ins.add_chart(pkg, sp, 1, ins.plain(g["title"])), ids))
    content += ins.notes_block(g, ids)
    for text in t["paragraphs"][2:]:
        content.append(ins.para([ins.run(text)], ids, align="both"))
    last = content[-1]
    ins._space_after(last, 0)
    # inside a one-cell box, keep-with-next chains make Word and LibreOffice move the whole box to a new page
    for e in content:
        for kn in e.iter(W + "keepNext"):
            kn.getparent().remove(kn)
    sect = body.find(W + "sectPr")
    note = ins.para([ins.run("For insertion in section 3.3, after the paragraph on tourism and services economies. "
                             "Referred to in sections 3.3 and 4.8 of the revised draft.", italic=True, size=18)],
                    ids, after=200)
    sect.addprevious(note)
    sect.addprevious(box_table(content, int(ins.TEXT_WIDTH_IN * 1440)))
    sect.addprevious(ins.para([], ids))   # Word needs a paragraph after a table at the end of a body
    pkg.save(dst)
    print("written", dst)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    main(Path(sys.argv[1]), Path(sys.argv[2]))
