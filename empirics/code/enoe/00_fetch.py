"""Download the ENOE quarterly zips from the release assets of wanderdata/enoe_data into the
uncommitted empirics/data/raw/enoe/ and record their SHA-256 in a manifest (D-046).

    python empirics/code/enoe/00_fetch.py            # CSV zips for the quarters in WINDOWS and CROSS_SECTIONS
    python empirics/code/enoe/00_fetch.py --all      # every asset of every release

The release holds INEGI's files for 2005 onward in four formats (csv, dbf, dta, sav); by default
only the CSV version of the quarters the study uses is downloaded.

Uses the GitHub REST API through the GitHub CLI (`gh api`), which must have access to the
repository. Files already present with the same size are not downloaded again.
"""
import hashlib
import json
import subprocess
import sys

from enoe_config import BORDER_QUARTERS, CROSS_SECTIONS, LADDER_YEARS, RAW, WINDOWS

REPO = "wanderdata/enoe_data"


def api(path, binary=False):
    cmd = ["gh", "api", path] + (["-H", "Accept: application/octet-stream"] if binary else [])
    r = subprocess.run(cmd, capture_output=True, check=True)
    return r.stdout if binary else json.loads(r.stdout)


def wanted(name, everything=False):
    if everything:
        return True
    n = name.lower()
    if not n.endswith("_csv.zip"):
        return False
    quarters = ({yq for qs in WINDOWS.values() for yq in qs} | set(CROSS_SECTIONS)
                | {(y, q) for y in LADDER_YEARS for q in (1, 2, 3, 4)} | set(BORDER_QUARTERS))
    return any(f"{y}trim{q}_csv" in n or f"{y}_trim{q}_csv" in n for y, q in quarters)


def assets(release_id):
    out, page = [], 1
    while True:
        a = api(f"repos/{REPO}/releases/{release_id}/assets?per_page=100&page={page}")
        out += a
        if len(a) < 100:
            return out
        page += 1


def main(args):
    RAW.mkdir(parents=True, exist_ok=True)
    everything = "--all" in args
    releases = api(f"repos/{REPO}/releases?per_page=100")
    if not releases:
        print(f"No releases found in {REPO}. Nothing done.")
        return 0
    manifest = []
    for r in releases:
        for a in assets(r["id"]):
            if not wanted(a["name"], everything):
                continue
            dest = RAW / a["name"]
            if not (dest.exists() and dest.stat().st_size == a["size"]):
                dest.write_bytes(api(f"repos/{REPO}/releases/assets/{a['id']}", binary=True))
            h = hashlib.sha256(dest.read_bytes()).hexdigest()
            manifest.append({"release": r["tag_name"], "file": a["name"], "bytes": a["size"], "sha256": h})
            print(f"{r['tag_name']}: {a['name']} ({a['size'] / 1e6:.1f} MB) {h[:12]}")
    (RAW / "manifest.json").write_text(json.dumps(manifest, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
