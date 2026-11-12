"""Download the ENOE quarterly zips from the release assets of wanderdata/enoe_data into the
uncommitted empirics/data/raw/enoe/ and record their SHA-256 in a manifest (D-046).

    python empirics/code/enoe/00_fetch.py            # all releases
    python empirics/code/enoe/00_fetch.py TAG ...    # selected releases

Needs the GitHub CLI (gh) with access to the repository. Files already present with the same
size are not downloaded again.
"""
import hashlib
import json
import subprocess
import sys

from enoe_config import RAW

REPO = "wanderdata/enoe_data"


def gh(*args):
    return subprocess.run(["gh", *args], capture_output=True, text=True, check=True).stdout


def main(tags):
    RAW.mkdir(parents=True, exist_ok=True)
    if not tags:
        tags = [r["tagName"] for r in json.loads(gh("release", "list", "-R", REPO, "--json", "tagName"))]
    manifest = []
    for t in tags:
        assets = json.loads(gh("release", "view", t, "-R", REPO, "--json", "assets"))["assets"]
        for a in assets:
            dest = RAW / a["name"]
            if not (dest.exists() and dest.stat().st_size == a["size"]):
                gh("release", "download", t, "-R", REPO, "-p", a["name"], "-D", str(RAW), "--clobber")
            h = hashlib.sha256(dest.read_bytes()).hexdigest()
            manifest.append({"release": t, "file": a["name"], "bytes": a["size"], "sha256": h})
            print(f"{t}: {a['name']} ({a['size'] / 1e6:.1f} MB) {h[:12]}")
    (RAW / "manifest.json").write_text(json.dumps(manifest, indent=1))


if __name__ == "__main__":
    main(sys.argv[1:])
