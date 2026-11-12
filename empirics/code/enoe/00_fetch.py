"""Download the ENOE quarterly zips from the release assets of wanderdata/enoe_data into the
uncommitted empirics/data/raw/enoe/ and record their SHA-256 in a manifest (D-046).

    python empirics/code/enoe/00_fetch.py            # all releases
    python empirics/code/enoe/00_fetch.py TAG ...    # selected releases

Uses the GitHub REST API through the GitHub CLI (`gh api`), which must have access to the
repository. Files already present with the same size are not downloaded again.
"""
import hashlib
import json
import subprocess
import sys

from enoe_config import RAW

REPO = "wanderdata/enoe_data"


def api(path, binary=False):
    cmd = ["gh", "api", path] + (["-H", "Accept: application/octet-stream"] if binary else [])
    r = subprocess.run(cmd, capture_output=True, check=True)
    return r.stdout if binary else json.loads(r.stdout)


def main(tags):
    RAW.mkdir(parents=True, exist_ok=True)
    releases = api(f"repos/{REPO}/releases?per_page=100")
    if tags:
        releases = [r for r in releases if r["tag_name"] in tags]
    if not releases:
        print(f"No releases found in {REPO}. Nothing done.")
        return 0
    manifest = []
    for r in releases:
        for a in r["assets"]:
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
