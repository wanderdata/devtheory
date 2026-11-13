"""Study 9.1 (job ladders): 01 link -> 02 flows -> 03 report. Fetch the data first with
empirics/code/enoe/00_fetch.py.

    python empirics/code/enoe/ladders/run_all.py
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

if __name__ == "__main__":
    for s in ["01_link.py", "02_flows.py", "03_report.py"]:
        print(f"== {s}")
        subprocess.run([sys.executable, str(HERE / s)], check=True, cwd=HERE)
