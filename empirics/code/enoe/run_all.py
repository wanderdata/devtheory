"""Run the ENOE job-ladder pipeline (WP09): 00 fetch -> 01 link -> 02 flows.

    python empirics/code/enoe/run_all.py [--no-fetch]

The microdata are not in this repository: 00_fetch.py downloads them from the release assets of
wanderdata/enoe_data into empirics/data/raw/enoe/. Without them the steps do nothing, so this
pipeline is not part of CI; its tests run on synthetic data.
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEPS = ["00_fetch.py", "01_link.py", "02_flows.py"]

if __name__ == "__main__":
    steps = STEPS[1:] if "--no-fetch" in sys.argv else STEPS
    for s in steps:
        print(f"== {s}")
        subprocess.run([sys.executable, str(HERE / s)], check=True, cwd=HERE)
