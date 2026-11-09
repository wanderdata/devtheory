"""Reproducibility check: after rebuilding outputs, compare them with the committed versions.

    python empirics/code/lp/run_all.py && python scripts/check_outputs.py

CSV files are compared numerically (relative tolerance 1e-9, so harmless floating-point
noise across machines passes); Markdown reports must match exactly; PNG figures are
skipped (their bytes depend on font and library builds). Exit code 1 if anything changed.
"""
import io
import subprocess
import sys

import numpy as np
import pandas as pd

PATHS = ["empirics/output", "empirics/data/processed", "empirics/data/interim"]


def changed_files():
    out = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all", "--", *PATHS],
                         capture_output=True, text=True, check=True).stdout
    return [line[3:] for line in out.splitlines() if line.strip()]


def committed(path):
    r = subprocess.run(["git", "show", f"HEAD:{path}"], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def same_csv(old, new):
    a = pd.read_csv(io.BytesIO(old), low_memory=False)
    b = pd.read_csv(new, low_memory=False)
    if list(a.columns) != list(b.columns) or len(a) != len(b):
        return False
    for c in a.columns:
        x, y = a[c], b[c]
        if pd.api.types.is_numeric_dtype(x) and pd.api.types.is_numeric_dtype(y):
            if not np.allclose(x.to_numpy(float), y.to_numpy(float), rtol=1e-9, atol=1e-12, equal_nan=True):
                return False
        elif not x.astype(str).equals(y.astype(str)):
            return False
    return True


def main():
    bad = []
    for f in changed_files():
        if f.endswith(".png"):
            continue
        old = committed(f)
        if old is None:
            bad.append(f"{f}: new file not in the commit")
        elif f.endswith(".csv"):
            if not same_csv(old, f):
                bad.append(f"{f}: values differ")
        else:
            bad.append(f"{f}: content differs")
    if bad:
        print("Outputs differ from the committed versions:\n  " + "\n  ".join(bad))
        sys.exit(1)
    print("All rebuilt outputs match the committed versions.")


if __name__ == "__main__":
    main()
