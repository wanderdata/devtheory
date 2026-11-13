"""Run the ENOE programme (WP09): fetch the data, then each study's pipeline.

    python empirics/code/enoe/run_all.py [--no-fetch]

The microdata are not in this repository: 00_fetch.py downloads them from the release assets of
wanderdata/enoe_data into empirics/data/raw/enoe/. Without them the steps do nothing, so this
pipeline is not part of CI; its tests run on synthetic data.
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STUDIES = ["ladders", "profiles", "productivity_ladder"]

if __name__ == "__main__":
    if "--no-fetch" not in sys.argv:
        subprocess.run([sys.executable, str(HERE / "00_fetch.py")], check=True, cwd=HERE)
    for st in STUDIES:
        print(f"==== study {st}")
        subprocess.run([sys.executable, str(HERE / st / "run_all.py")], check=True, cwd=HERE / st)
