"""Download the raw source files into empirics/data/raw/<scope>_lp/.

Run this on a machine that can reach unstats.un.org and rplumber.ilo.org.
(The project's cloud workspace cannot; there the files were attached by hand,
see the research log for 2026-11-05.)

    python empirics/code/lp/01_download.py
"""
import sys
import urllib.request

from config import RAW, SOURCES


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    for key, s in SOURCES.items():
        dest = RAW / s["file"]
        if dest.exists():
            print(f"[skip] {dest.name} exists")
            continue
        print(f"[get ] {key}: {s['url']}")
        try:
            urllib.request.urlretrieve(s["url"], dest)
        except Exception as e:  # report and continue with the others
            print(f"[fail] {key}: {e}", file=sys.stderr)
            continue
        print(f"[ok  ] {dest.name} ({dest.stat().st_size/1e6:.1f} MB)")


if __name__ == "__main__":
    main()
