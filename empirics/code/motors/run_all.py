"""Rebuild every output of the development-motors project (WP07).

    python empirics/code/motors/run_all.py

01 panel -> 02 replication -> 03 questions 1-3 -> 04 sectors (question 4) -> 05 specification curve.
Stops at the first failing step.
"""
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEPS = ["01_build_panel.py", "02_replicate.py", "03_questions.py", "04_sectors.py", "05_speccurve.py"]

if __name__ == "__main__":
    for step in STEPS:
        print(f"[motors] {step}", flush=True)
        r = subprocess.run([sys.executable, str(HERE / step)], cwd=HERE, env=dict(os.environ, MPLBACKEND="Agg"),
                           stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
        if r.returncode:
            sys.stderr.write(r.stderr[-3000:])
            raise SystemExit(f"[motors] {step} failed (exit {r.returncode})")
    print("done")
