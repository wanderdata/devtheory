"""Study 9.4, step 0: municipal boundaries of the six border states, the ZLFN list, and each
municipality's signed distance to the edge of the zone (pre-analysis plan §4, D-054).

    python empirics/code/enoe/border_mw/00_geo.py

Source: CONABIO's 2020 municipal boundaries (derived from INEGI's Marco Geoestadístico), as
state GeoJSON files in the public repository PhantomInsights/mexico-geojson. They are downloaded
unchanged into the uncommitted empirics/data/raw/geo_mx/ with a SHA-256 manifest. Outputs
(committed, small):
  empirics/output/enoe/border_mw/municipalities.geojson  simplified boundaries for the maps
  empirics/output/enoe/border_mw/municipalities.csv      ent, mun, name, zlfn, centroid, distance
"""
import hashlib
import json
import sys
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1]))

import pandas as pd  # noqa: E402
from shapely.geometry import MultiPolygon, Polygon, mapping, shape  # noqa: E402
from shapely.geometry.polygon import orient  # noqa: E402
from shapely import set_precision  # noqa: E402
from shapely.affinity import scale  # noqa: E402
from shapely.ops import unary_union  # noqa: E402

from enoe_config import OUTPUT_ROOT, ROOT  # noqa: E402

RAW = ROOT / "empirics" / "data" / "raw" / "geo_mx"
OUT = OUTPUT_ROOT / "border_mw"
BASE = "https://raw.githubusercontent.com/PhantomInsights/mexico-geojson/main/2020/states/"
STATES = {3: "Baja California Sur", 2: "Baja California", 5: "Coahuila de Zaragoza", 8: "Chihuahua", 19: "Nuevo León", 26: "Sonora",
          28: "Tamaulipas"}

# Municipalities of the Zona Libre de la Frontera Norte (decree of 31 December 2018, art. 1),
# by state, as written in the decree (accents removed). Matched to INEGI codes by name below.
ZLFN = {2: ["ensenada", "playas de rosarito", "mexicali", "tecate", "tijuana"],
        26: ["san luis rio colorado", "puerto penasco", "general plutarco elias calles", "caborca", "altar", "saric",
             "nogales", "santa cruz", "cananea", "naco", "agua prieta"],
        8: ["janos", "ascension", "juarez", "praxedis g. guerrero", "guadalupe", "coyame del sotol", "ojinaga",
            "manuel benavides"],
        5: ["ocampo", "acuna", "zaragoza", "jimenez", "piedras negras", "nava", "guerrero", "hidalgo"],
        19: ["anahuac"],
        28: ["nuevo laredo", "guerrero", "mier", "miguel aleman", "camargo", "gustavo diaz ordaz", "reynosa",
             "rio bravo", "valle hermoso", "matamoros"]}
EDGE_ONLY = {3}                # Baja California Sur: only to locate the zone's southern edge in Baja California
MERGE = {(2, 6): (2, 1)}       # San Quintín (created 2020) back into Ensenada, as in ENOE 2016-2020
SIMPLIFY_DEG = 0.01            # display tolerance, about 1 km


def ascii_lower(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower().strip()


def fetch():
    RAW.mkdir(parents=True, exist_ok=True)
    manifest = []
    for ent, name in STATES.items():
        dest = RAW / f"{ent:02d}.json"
        if not dest.exists():
            url = BASE + urllib.parse.quote(name) + ".json"
            dest.write_bytes(urllib.request.urlopen(url, timeout=120).read())
        manifest.append({"ent": ent, "file": dest.name, "sha256": hashlib.sha256(dest.read_bytes()).hexdigest()})
    (RAW / "manifest.json").write_text(json.dumps(manifest, indent=1))


def km(geom, lat0=29.0):
    """Equirectangular projection in km around latitude lat0 (adequate for distances of a few
    hundred km along the border)."""
    import math
    c = math.cos(math.radians(lat0))
    return scale(geom, xfact=111.32 * c, yfact=110.57, origin=(0, 0))


def clockwise(g):
    """Exterior rings clockwise, as d3 (and so Plotly's geo maps) expects; counter-clockwise rings
    are drawn as the whole globe minus the polygon."""
    if isinstance(g, Polygon):
        return orient(g, sign=-1.0)
    if isinstance(g, MultiPolygon):
        return MultiPolygon([orient(p, sign=-1.0) for p in g.geoms])
    return g


def main():
    fetch()
    rows, geoms = [], {}
    for ent in STATES:
        for f in json.loads((RAW / f"{ent:02d}.json").read_text(encoding="utf-8"))["features"]:
            p = f["properties"]
            k = (int(p["CVE_ENT"]), int(p["CVE_MUN"]))
            k = MERGE.get(k, k)
            g = shape(f["geometry"]).buffer(0)
            geoms[k] = unary_union([geoms[k], g]) if k in geoms else g
            if (int(p["CVE_ENT"]), int(p["CVE_MUN"])) not in MERGE:
                rows.append({"ent": k[0], "mun": k[1], "name": p["NOM_MUN"], "key": ascii_lower(p["NOM_MUN"])})
    m = pd.DataFrame(rows).drop_duplicates(["ent", "mun"])
    m["zlfn"] = False
    for ent, names in ZLFN.items():
        for n in names:
            hit = (m["ent"] == ent) & (m["key"] == n)
            if hit.sum() != 1:
                raise SystemExit(f"ZLFN municipality not matched uniquely: {ent} {n}")
            m.loc[hit, "zlfn"] = True
    assert m["zlfn"].sum() == 43
    zone = km(unary_union([geoms[(e, u)] for e, u in m.loc[m["zlfn"], ["ent", "mun"]].itertuples(index=False)]))
    rest = km(unary_union([geoms[(e, u)] for e, u in m.loc[~m["zlfn"], ["ent", "mun"]].itertuples(index=False)]))
    edge = zone.boundary.intersection(rest.boundary.buffer(0.5))     # the zone's edge with the rest of Mexico
    out = []
    for r in m.itertuples(index=False):
        g = geoms[(r.ent, r.mun)]
        c = g.centroid
        d = km(c).distance(edge)
        out.append({"ent": r.ent, "mun": r.mun, "name": r.name, "zlfn": r.zlfn, "lon": c.x, "lat": c.y,
                    "dist_km": -d if r.zlfn else d})
    out = pd.DataFrame(out)
    out = out[~out["ent"].isin(EDGE_ONLY)].sort_values(["ent", "mun"])
    OUT.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT / "municipalities.csv", index=False, float_format="%.4f")
    feats = []
    for r in out.itertuples(index=False):
        g = geoms[(r.ent, r.mun)].simplify(SIMPLIFY_DEG, preserve_topology=True)
        g = set_precision(g, 0.001)
        g = clockwise(g)
        feats.append({"type": "Feature", "id": f"{r.ent:02d}{r.mun:03d}",
                      "properties": {"name": r.name, "zlfn": bool(r.zlfn)}, "geometry": mapping(g)})
    (OUT / "municipalities.geojson").write_text(json.dumps({"type": "FeatureCollection", "features": feats},
                                                           separators=(",", ":")))
    print(out.groupby("zlfn")["dist_km"].describe().round(1).to_string())
    print(f"geojson {(OUT / 'municipalities.geojson').stat().st_size / 1e6:.2f} MB")


if __name__ == "__main__":
    main()
