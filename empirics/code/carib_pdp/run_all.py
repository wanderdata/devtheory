"""Rebuild every output of the Caribbean PDP report figures (D-072).

    python empirics/code/carib_pdp/run_all.py

Requires the lp pipeline's Caribbean outputs (python empirics/code/lp/run_all.py carib).
Steps: 01 figure data -> 02 SVG figures -> 03 Excel workbook. Step 05 (insert into the
report) is run by hand with the path of the report, which is kept outside the repository.
"""
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEPS = ["01_figure_data.py", "02_svg_figures.py", "03_workbook.py"]

if __name__ == "__main__":
    env = dict(os.environ, MPLBACKEND="Agg")
    for step in STEPS:
        print(step, flush=True)
        r = subprocess.run([sys.executable, str(HERE / step)], cwd=HERE, env=env)
        if r.returncode:
            raise SystemExit(f"{step} failed (exit {r.returncode})")
    print("done")
