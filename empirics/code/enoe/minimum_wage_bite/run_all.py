"""Study 9.8 (minimum-wage bite): 01 extract -> 02 cells -> 03 difference-in-differences -> 04 report.
Needs study 9.4's border-zone municipality list and study 9.7's activity classification.

    python empirics/code/enoe/minimum_wage_bite/run_all.py
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

if __name__ == "__main__":
    for s in ["01_extract.py", "02_cells.py", "03_did.py", "03b_diagnostics.py", "04_report.py"]:
        print(f"== {s}")
        subprocess.run([sys.executable, str(HERE / s)], check=True, cwd=HERE)
