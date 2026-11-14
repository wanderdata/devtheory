"""Study 9.4 (2019 border minimum wage): 00 geography -> 01 extract -> 02 cells -> 03 DiD -> 04 maps -> 05 report.

    python empirics/code/enoe/border_mw/run_all.py
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

if __name__ == "__main__":
    for s in ["00_geo.py", "01_extract.py", "02_cells.py", "03_did.py", "04_maps.py", "05_report.py"]:
        print(f"== {s}")
        subprocess.run([sys.executable, str(HERE / s)], check=True, cwd=HERE)
