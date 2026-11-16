"""Study 9.7: activity classifications (pre-analysis plan §2).

FINE: the PIBE activity series that ENOE's industry code (`p4a`) can be matched to.
MAIN: the 20 groups of the main classification, as unions of FINE codes.
MEITEF: the activity groups of INEGI's informal-economy accounts, as unions of FINE codes.

ENOE codes that do not identify a FINE activity are distributed within state, year and formality
segment in proportion to specified employment: three-digit codes ending in 9 (unspecified within a
sector) and code 3380 within their two-digit sector (all of manufacturing for 3380, which ENOE uses
mostly in the northern border states); codes 9700, 9800 and 9999 across all non-oil activities.
Codes 211x (oil and gas extraction; ENOE uses 2110) are excluded with oil value added.
"""
import numpy as np
import pandas as pd

FINE = ["111", "112", "114", "otros11", "21np", "22", "23", "311", "312", "313_314", "315_316", "321",
        "322_323", "324_326", "327", "331_332", "333_336", "337", "339", "43", "46", "48_49", "51", "52",
        "53", "54", "55", "56", "61", "62", "71", "72", "81", "93"]

MAIN = {
    "Agriculture, forestry and fishing": ["111", "112", "114", "otros11"],
    "Non-oil mining": ["21np"],
    "Utilities": ["22"],
    "Construction": ["23"],
    "Food, beverages and tobacco": ["311", "312"],
    "Textiles, clothing, wood, paper and furniture": ["313_314", "315_316", "321", "322_323", "337"],
    "Petroleum products, chemicals, minerals and metals": ["324_326", "327", "331_332"],
    "Machinery, electrical and transport equipment, other": ["333_336", "339"],
    "Wholesale trade": ["43"],
    "Retail trade": ["46"],
    "Transport and storage": ["48_49"],
    "Information": ["51"],
    "Finance and insurance": ["52"],
    "Real estate": ["53"],
    "Professional, corporate and support services": ["54", "55", "56"],
    "Education": ["61"],
    "Health and social assistance": ["62"],
    "Accommodation and food": ["72"],
    "Arts, recreation and other services": ["71", "81"],
    "Government": ["93"],
}

MEITEF = {"11": ["111", "112", "114", "otros11"], "21": ["21np"], "22": ["22"], "23": ["23"],
          "31-33": ["311", "312", "313_314", "315_316", "321", "322_323", "324_326", "327", "331_332",
                    "333_336", "337", "339"],
          "43-46": ["43", "46"], "48-49": ["48_49"], "51": ["51"], "52": ["52"], "53": ["53"], "54": ["54"],
          "55-56": ["55", "56"], "61": ["61"], "62": ["62"], "71": ["71"], "72": ["72"], "81": ["81"], "93": ["93"]}

MANUF = MEITEF["31-33"]
SECTOR2 = {"11": MAIN["Agriculture, forestry and fishing"], "21": ["21np"], "22": ["22"], "23": ["23"],
           "31": MANUF, "32": MANUF, "33": MANUF, "43": ["43"], "46": ["46"], "48": ["48_49"], "49": ["48_49"],
           "51": ["51"], "52": ["52"], "53": ["53"], "54": ["54"], "55": ["55"], "56": ["56"], "61": ["61"],
           "62": ["62"], "71": ["71"], "72": ["72"], "81": ["81"], "93": ["93"]}

_MANUF3 = {311: "311", 312: "312", 313: "313_314", 314: "313_314", 315: "315_316", 316: "315_316", 321: "321",
           322: "322_323", 323: "322_323", 324: "324_326", 325: "324_326", 326: "324_326", 327: "327",
           331: "331_332", 332: "331_332", 333: "333_336", 334: "333_336", 335: "333_336", 336: "333_336",
           337: "337", 339: "339"}
_AGRI3 = {111: "111", 112: "112", 114: "114", 113: "otros11", 115: "otros11"}


def fine_code(p4a):
    """Vectorised map from ENOE `p4a` to a FINE code, 'OIL', 'U<2-digit>' (unspecified within a sector)
    or 'UALL' (unspecified)."""
    p = pd.Series(np.asarray(p4a), dtype="int64")
    s3, s2 = p // 10, p // 100
    out = pd.Series("UALL", index=p.index, dtype=object)
    two = {21: "21np", 22: "22", 23: "23", 43: "43", 46: "46", 48: "48_49", 49: "48_49", 51: "51", 52: "52",
           53: "53", 54: "54", 55: "55", 56: "56", 61: "61", 62: "62", 71: "71", 72: "72", 81: "81", 93: "93"}
    m2 = s2.map(two)
    out[m2.notna()] = m2[m2.notna()]
    agri = s3.map(_AGRI3)
    out[s2 == 11] = "U11"
    out[agri.notna()] = agri[agri.notna()]
    man = s3.map(_MANUF3)
    out[s2.isin([31, 32, 33])] = "U31"
    out[man.notna()] = man[man.notna()]
    # three-digit codes ending in 9 outside manufacturing (339 is a real SCIAN subsector)
    unspec = (s3 % 10 == 9) & ~s2.isin([31, 32, 33]) & s2.isin(list(two) + [11])
    out[unspec] = "U" + s2[unspec].astype(str)
    out[s3 == 211] = "OIL"  # ENOE codes oil and gas extraction as 2110
    out[s2.isin([97, 98, 99]) | (p <= 0)] = "UALL"
    return out.values


def distribute(df, keys, value_cols, code="act"):
    """Distribute rows whose `code` is 'U..' over FINE codes in proportion to specified values within
    `keys`. Returns a frame with FINE codes only (OIL dropped)."""
    df = df[df[code] != "OIL"]
    spec = df[df[code].isin(FINE)].groupby(keys + [code], as_index=False)[value_cols].sum()
    uns = df[~df[code].isin(FINE)].groupby(keys + [code], as_index=False)[value_cols].sum()
    out = [spec]
    for u, g in uns.groupby(code):
        targets = FINE if u == "UALL" else SECTOR2[u[1:]]
        base = spec[spec[code].isin(targets)]
        share = base.copy()
        tot = base.groupby(keys)[value_cols].transform("sum")
        share[value_cols] = base[value_cols] / tot.replace(0, np.nan)
        m = share.merge(g.drop(columns=code), on=keys, suffixes=("_s", ""))
        for c in value_cols:
            m[c] = m[c + "_s"].fillna(0) * m[c]
        out.append(m[keys + [code] + value_cols])
    res = pd.concat(out).groupby(keys + [code], as_index=False)[value_cols].sum()
    return res


def to_main(fine):
    inv = {f: g for g, fs in MAIN.items() for f in fs}
    return pd.Series(fine).map(inv).values
