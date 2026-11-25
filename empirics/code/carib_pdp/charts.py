"""Chart specifications for the report's Excel charts, with two renderers.

A spec holds the plotted data and formatting. `add_to_workbook` draws it as a native chart
in an XlsxWriter workbook (the deliverable workbook). `word_chart_parts` draws the same chart
with python-pptx and returns its DrawingML chart part and embedded worksheet, which
05_insert_docx.py places in the report as a Word chart ("Edit Data" opens the worksheet).
Formatting follows the report: no title inside the chart (titles and notes are document
text), Calibri 8 pt, light gridlines, categorical colours in a fixed order.
"""
import io
import re
import zipfile
from dataclasses import dataclass, field

from lxml import etree

COLOURS = ["#257DE0", "#F47230", "#00B894", "#F2A600"]   # fixed categorical order
INK, MUTED, GRID = "#191919", "#666666", "#D9D9D9"
FONT, SIZE = "Calibri", 8


@dataclass
class Spec:
    key: str                      # sheet / file stem, e.g. "graph2a"
    categories: list              # category labels, top to bottom as they should appear
    series: dict                  # name -> list of values (same length as categories)
    number_format: str = "0.0"
    cell_format: str | None = None   # format of the data cells, if different from the axis
    axis_title: str = ""
    log: bool = False             # log-10 value axis, category axis crossing at 1
    axis_min: float | None = None
    axis_max: float | None = None
    major_unit: float | None = None
    data_labels: bool = False
    legend: bool = True
    width_in: float = 6.5
    height_in: float = 3.2
    gap: int = 60
    notes: list = field(default_factory=list)


# --------------------------------------------------------------------------- XlsxWriter
def add_to_workbook(wb, ws, spec, first_row, first_col, anchor):
    """Write the spec's data at (first_row, first_col) of ws and insert its chart at anchor."""
    from xlsxwriter.utility import xl_rowcol_to_cell
    head = wb.add_format({"bold": True, "font_name": FONT, "font_size": 9, "bottom": 1})
    body = wb.add_format({"font_name": FONT, "font_size": 9})
    num = wb.add_format({"font_name": FONT, "font_size": 9, "num_format": spec.cell_format or spec.number_format})
    ws.write(first_row, first_col, "", head)
    for j, name in enumerate(spec.series):
        ws.write(first_row, first_col + 1 + j, name, head)
    for i, c in enumerate(spec.categories):
        ws.write(first_row + 1 + i, first_col, c, body)
        for j, vals in enumerate(spec.series.values()):
            ws.write_number(first_row + 1 + i, first_col + 1 + j, float(vals[i]), num)
    chart = wb.add_chart({"type": "bar"})
    n = len(spec.categories)
    sheet = ws.get_name()
    for j, name in enumerate(spec.series):
        col = first_col + 1 + j
        s = {"name": [sheet, first_row, col],
             "categories": [sheet, first_row + 1, first_col, first_row + n, first_col],
             "values": [sheet, first_row + 1, col, first_row + n, col],
             "fill": {"color": COLOURS[j]}, "border": {"none": True}, "gap": spec.gap, "overlap": -5}
        if spec.data_labels:
            s["data_labels"] = {"value": True, "num_format": spec.number_format,
                                "font": {"name": FONT, "size": SIZE, "color": INK}}
        chart.add_series(s)
    val = {"num_format": spec.number_format, "num_font": {"name": FONT, "size": SIZE, "color": INK},
           "line": {"none": True}, "major_gridlines": {"visible": True, "line": {"color": GRID, "width": 0.5}},
           "major_tick_mark": "none"}
    if spec.axis_title:
        val["name"] = spec.axis_title
        val["name_font"] = {"name": FONT, "size": SIZE, "bold": False, "color": MUTED}
    if spec.log:
        val["log_base"] = 10
        val["crossing"] = 1   # XlsxWriter writes this as the category axis crossing the value axis at 1
    for k, v in (("min", spec.axis_min), ("max", spec.axis_max), ("major_unit", spec.major_unit)):
        if v is not None:
            val[k] = v
    chart.set_x_axis(val)   # in a bar chart the x axis is the value axis
    chart.set_y_axis({"reverse": True, "crossing": "max", "interval_unit": 1, "num_font": {"name": FONT, "size": SIZE, "color": INK},
                      "line": {"color": MUTED, "width": 0.75}, "major_tick_mark": "none",
                      "label_position": "low"})
    if spec.legend and len(spec.series) > 1:
        chart.set_legend({"position": "top", "font": {"name": FONT, "size": SIZE, "color": INK}})
    else:
        chart.set_legend({"none": True})
    chart.set_title({"none": True})
    chart.set_chartarea({"border": {"none": True}})
    chart.set_plotarea({"border": {"none": True}})
    chart.set_size({"width": int(spec.width_in * 96), "height": int(spec.height_in * 96)})
    ws.insert_chart(anchor, chart)
    return xl_rowcol_to_cell(first_row + n, first_col + len(spec.series))


# --------------------------------------------------------------------------- python-pptx -> Word
def _rgb(h):
    from pptx.dml.color import RGBColor
    return RGBColor.from_string(h.lstrip("#"))


def _finish(xml, spec):
    """Edits python-pptx has no API for: log scale, every category label shown, no chart border."""
    C = "{http://schemas.openxmlformats.org/drawingml/2006/chart}"
    A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
    root = etree.fromstring(xml)
    if spec.log:
        for sc in root.iter(C + "scaling"):
            if sc.getparent().tag == C + "valAx":
                lb = etree.Element(C + "logBase")
                lb.set("val", "10")
                sc.insert(0, lb)
    for va in root.iter(C + "valAx"):   # value axis at the bottom when categories run top-down
        cr = va.find(C + "crosses")
        if cr is not None:
            cr.set("val", "max")
    for cat in root.iter(C + "catAx"):
        skip = etree.Element(C + "tickLblSkip")
        skip.set("val", "1")
        nm = cat.find(C + "noMultiLvlLbl")
        if nm is not None:
            nm.addprevious(skip)
        else:
            cat.append(skip)
    chart = root.find(C + "chart")
    if root.find(C + "roundedCorners") is None:
        rc = etree.Element(C + "roundedCorners")
        rc.set("val", "0")
        chart.addprevious(rc)
    sp = root.find(C + "spPr")
    if sp is None:
        sp = etree.Element(C + "spPr")
        chart.addnext(sp)
    ln = etree.SubElement(sp, A + "ln")
    etree.SubElement(ln, A + "noFill")
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)


def word_chart_parts(spec):
    """Return (chart_xml: bytes, embedded_xlsx: bytes) for a Word chart drawn from spec."""
    from pptx import Presentation
    from pptx.chart.data import CategoryChartData
    from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION, XL_TICK_LABEL_POSITION
    from pptx.enum.chart import XL_TICK_MARK
    from pptx.util import Inches, Pt

    data = CategoryChartData(number_format=spec.number_format)
    data.categories = spec.categories
    for name, vals in spec.series.items():
        data.add_series(name, [float(v) for v in vals])
    prs = Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    gf = slide.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, 0, 0, Inches(spec.width_in), Inches(spec.height_in), data)
    ch = gf.chart
    ch.font.name, ch.font.size = FONT, Pt(SIZE)
    ch.font.color.rgb = _rgb(INK)
    ch.has_title = False
    plot = ch.plots[0]
    plot.gap_width, plot.overlap = spec.gap, -5
    plot.vary_by_categories = False
    for j, s in enumerate(plot.series):
        s.format.fill.solid()
        s.format.fill.fore_color.rgb = _rgb(COLOURS[j])
        s.format.line.fill.background()
        s.invert_if_negative = False
    if spec.data_labels:
        plot.has_data_labels = True
        dl = plot.data_labels
        dl.number_format, dl.number_format_is_linked = spec.number_format, False
        dl.position = XL_LABEL_POSITION.OUTSIDE_END
        dl.font.size, dl.font.name = Pt(SIZE), FONT
    cat, val = ch.category_axis, ch.value_axis
    cat.reverse_order = True
    cat.major_tick_mark = XL_TICK_MARK.NONE
    cat.tick_label_position = XL_TICK_LABEL_POSITION.LOW
    cat.format.line.color.rgb = _rgb(MUTED)
    val.has_major_gridlines = True
    val.major_gridlines.format.line.color.rgb = _rgb(GRID)
    val.major_gridlines.format.line.width = Pt(0.5)
    val.format.line.fill.background()
    val.major_tick_mark = XL_TICK_MARK.NONE
    val.tick_labels.number_format, val.tick_labels.number_format_is_linked = spec.number_format, False
    if spec.axis_min is not None:
        val.minimum_scale = spec.axis_min
    if spec.axis_max is not None:
        val.maximum_scale = spec.axis_max
    if spec.major_unit is not None:
        val.major_unit = spec.major_unit
    if spec.axis_title:
        val.has_title = True
        tf = val.axis_title.text_frame
        tf.text = spec.axis_title
        r = tf.paragraphs[0].runs[0]
        r.font.size, r.font.bold, r.font.name = Pt(SIZE), False, FONT
        r.font.color.rgb = _rgb(MUTED)
    if spec.log:
        val.crosses_at = 1
    if spec.legend and len(spec.series) > 1:
        ch.has_legend = True
        ch.legend.position = XL_LEGEND_POSITION.TOP
        ch.legend.include_in_layout = False
        ch.legend.font.size, ch.legend.font.name = Pt(SIZE), FONT
    else:
        ch.has_legend = False
    buf = io.BytesIO()
    prs.save(buf)
    z = zipfile.ZipFile(buf)
    chart_name = next(n for n in z.namelist() if n.startswith("ppt/charts/chart") and n.endswith(".xml"))
    xml = z.read(chart_name)
    xml = _finish(xml, spec)
    # python-pptx writes negative axis ids, which the schema (xs:unsignedInt) does not allow
    xml = re.sub(rb'(<c:(?:axId|crossAx) val=")-(\d+)"', rb'\1\2"', xml)
    emb = next(n for n in z.namelist() if n.startswith("ppt/embeddings/"))
    return xml, z.read(emb)
