"""Study 9.6, step 0: state boundaries for the maps, dissolved from CONABIO's 2020 municipal
boundaries (the files used in study 9.4, all 32 states).

    python empirics/code/enoe/states/00_geo.py

Inputs: empirics/data/raw/geo_mx/EE.json (uncommitted; downloaded from PhantomInsights/mexico-geojson
if missing). Output: empirics/output/enoe/states/states.geojson (simplified, committed).
"""
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))

from shapely import set_precision  # noqa: E402
from shapely.geometry import mapping, shape  # noqa: E402
from shapely.ops import unary_union  # noqa: E402

import gdp  # noqa: E402

RAW = gdp.ROOT / "empirics" / "data" / "raw" / "geo_mx"
OUT = gdp.ROOT / "empirics" / "output" / "enoe" / "states"
BASE = "https://raw.githubusercontent.com/PhantomInsights/mexico-geojson/main/2020/states/"
SIMPLIFY_DEG = 0.02


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    feats = []
    for ent, name in gdp.STATES.items():
        f = RAW / f"{ent:02d}.json"
        if not f.exists():
            f.write_bytes(urllib.request.urlopen(BASE + urllib.parse.quote(name) + ".json", timeout=120).read())
        g = unary_union([shape(x["geometry"]).buffer(0) for x in json.loads(f.read_text(encoding="utf-8"))["features"]])
        g = set_precision(g.simplify(SIMPLIFY_DEG, preserve_topology=True), 0.001)
        feats.append({"type": "Feature", "id": f"{ent:02d}", "properties": {"name": name, "short": gdp.SHORT[ent]},
                      "geometry": mapping(g)})
    (OUT / "states.geojson").write_text(json.dumps({"type": "FeatureCollection", "features": feats}, separators=(",", ":")))
    print(f"states.geojson {(OUT / 'states.geojson').stat().st_size / 1e6:.2f} MB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
