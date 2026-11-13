"""Study 9.2 (experience-earnings profiles): 01 extract -> 02 profiles -> 03 panel -> 04 diagnostics
-> 05 report. Needs the ENOE first-quarter files (00_fetch.py) and, for step 03, the linked panels
of study 9.1.

    python empirics/code/enoe/profiles/run_all.py
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

if __name__ == "__main__":
    for s in ["01_extract.py", "02_profiles.py", "03_panel.py", "04_diagnostics.py", "05_report.py"]:
        print(f"== {s}")
        subprocess.run([sys.executable, str(HERE / s)], check=True, cwd=HERE)
