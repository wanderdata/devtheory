"""Rebuild every output of the labour-productivity project, for both scopes.

    python empirics/code/lp/run_all.py            # carib and lac
    python empirics/code/lp/run_all.py lac        # one scope

Steps (each a separate script, run in a fresh process with LP_SCOPE set):
02 extract -> 03 panel -> 03b grid-B employment -> 04 validation -> 05 decompositions
-> 06 labour-market series -> 07 regional summary (lac only) -> 08 output per working-age
person and productivity ladders -> 09 relative prices by sector.
01_download.py is not run: the sources are committed in empirics/data/source/ (D-029).
Stops at the first failing step.
"""
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEPS = ["02_extract.py", "03_build_panel.py", "03b_build_panel5.py", "04_validate.py",
         "05_decompose.py", "06_extract_labour.py", "07_lac_summary.py", "08_ladder.py", "09_baumol.py"]


def run(scope):
    env = dict(os.environ, LP_SCOPE=scope, MPLBACKEND="Agg")
    for step in STEPS:
        if step == "07_lac_summary.py" and scope != "lac":
            continue
        print(f"[{scope}] {step}", flush=True)
        r = subprocess.run([sys.executable, str(HERE / step)], env=env, cwd=HERE,
                           stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
        if r.returncode:
            sys.stderr.write(r.stderr[-3000:])
            raise SystemExit(f"[{scope}] {step} failed (exit {r.returncode})")


if __name__ == "__main__":
    for sc in (sys.argv[1:] or ["carib", "lac"]):
        run(sc)
    print("done")
