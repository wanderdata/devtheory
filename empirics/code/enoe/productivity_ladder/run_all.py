"""Study 9.3 (productivity ladder with formal and informal steps): 01 extract -> 02 ladder -> 03 report.

    python empirics/code/enoe/productivity_ladder/run_all.py
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

if __name__ == "__main__":
    for s in ["01_extract.py", "02_ladder.py", "03_report.py"]:
        print(f"== {s}")
        subprocess.run([sys.executable, str(HERE / s)], check=True, cwd=HERE)
