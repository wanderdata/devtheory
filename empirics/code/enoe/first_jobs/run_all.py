"""Study 9.5 (first jobs): 01 extract -> 02 panels -> 03 estimates -> 04 report.

    python empirics/code/enoe/first_jobs/run_all.py
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

if __name__ == "__main__":
    for s in ["01_extract.py", "02_panels.py", "03_estimates.py", "04_report.py"]:
        print(f"== {s}")
        subprocess.run([sys.executable, str(HERE / s)], check=True, cwd=HERE)
