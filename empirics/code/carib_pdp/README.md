# carib_pdp: figures for the Caribbean productive development policy report

Data, figures and annex tables for the report *Productive Development Policy in the Caribbean* (draft narrative, October 2026). The report itself is kept outside the repository. Decisions in D-072 and D-073; open items in OQ-90 and OQ-91.

**Run everything:** `python empirics/code/carib_pdp/run_all.py` (needs the Caribbean outputs of [`lp`](../lp/README.md)). Tests: `pytest empirics/code/carib_pdp`.

| Step | What | Output (`empirics/output/carib_pdp/`) |
|---|---|---|
| `01_figure_data.py` | Graph 1: McMillan–Rodrik terms by country (from `lp`) and pooled by production type (with `lp`'s own pooling function), 2000–2019 and 2019–2024, at chained, initial-year and final-year prices. Graph 2: employment shares and relative productivity by sector and type, 2024. Graphs 4 and 5: counts cited in the draft (`inputs/draft_counts.csv`). Section 3.4: total employment, 2024 | `data/*.csv` |
| `02_svg_figures.py` | Graph 1 as SVG, with text kept as editable text in Calibri | `figures/graph1_decomposition.svg` |
| `03_workbook.py` | Excel workbook: one sheet per graph and annex table, with title, unit, source and notes, and native charts for graphs 2, 4 and 5 | `caribbean_pdp_graphs.xlsx` |
| `05_insert_docx.py` | Run by hand: `python 05_insert_docx.py DRAFT.docx OUT.docx`. Replaces the graph placeholders with ECLAC-style text (label, title, unit; source and notes) around the figures, revises sections 3.1, 3.2 and 3.4, adds annex tables A.1–A.3 and comments on the placeholders still without data. All changes are tracked (author "Claude") | the report (not committed) |
| `06_box_docx.py` | Run by hand: `python 06_box_docx.py DRAFT.docx OUT.docx`. Box 1 (productivity in the tourism and services economies, Graph B1) as a separate document in the report's styles (D-073) | the box (not committed) |
| `config.py`, `texts.py`, `specs.py`, `charts.py` | Settings and production types; titles, notes and report text formatted from the data; chart specifications; Excel and Word chart renderers | — |

Production types (D-072): resource and energy (Guyana, Suriname, Trinidad and Tobago); tourism and services (the Bahamas, Barbados, Saint Lucia, Saint Vincent and the Grenadines, and Antigua and Barbuda, Dominica, Grenada and Saint Kitts and Nevis, which have no sector employment series); mixed (Jamaica, Belize); other Caribbean (the Dominican Republic, Haiti, Cuba). Cuba is shown by country but never pooled (D-033).

Graphs 2, 4 and 5 go into the report as Word charts with an embedded worksheet, drawn from the same specifications as the workbook charts. Graph 1 goes in as SVG, with the bitmap fallback the .docx format requires for versions of Word that cannot display SVG. The SVG is not byte-compared by `scripts/check_outputs.py`, because its layout depends on the fonts installed.
