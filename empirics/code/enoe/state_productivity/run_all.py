"""Study 9.7 (productivity by state and activity): 00 MEITEF -> 01 extract -> 01b population -> 02 panel -> 03 estimates
-> 04 pass-through -> 05 report.

    python empirics/code/enoe/state_productivity/run_all.py
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

if __name__ == "__main__":
    for s in ["00_meitef.py", "01_extract.py", "01b_population.py", "02_panel.py", "03_estimates.py", "04_passthrough.py", "05_report.py"]:
        print(f"== {s}")
        subprocess.run([sys.executable, str(HERE / s)], check=True, cwd=HERE)
