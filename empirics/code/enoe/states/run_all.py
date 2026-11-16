"""Study 9.6 (states): 00 geography -> 01 extract -> 02 panels -> 03 estimates -> 04 report.

    python empirics/code/enoe/states/run_all.py
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

if __name__ == "__main__":
    for s in ["00_geo.py", "01_extract.py", "02_panels.py", "03_estimates.py", "04_report.py"]:
        print(f"== {s}")
        subprocess.run([sys.executable, str(HERE / s)], check=True, cwd=HERE)
