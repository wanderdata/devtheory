"""Sector concordance: ILO economic-activity codes and UN AMA indicators -> 7 target sectors.

Target sectors follow the UN National Accounts Main Aggregates (AMA) grouping,
which uses ISIC Rev.3 letters (see config.SECTORS). Known approximations when
mapping ISIC Rev.4 to these groups (D-020):
  * ISIC4 J (information and communication) -> TSC. In ISIC3, telecoms were in I
    (TSC) but publishing was in D (manufacturing) and computing in K (OTH).
  * ISIC4 E (water, sewerage, waste) -> MIU. In ISIC3, sewage/refuse was in O (OTH).
  * ISIC4 H (transport, storage) -> TSC; ISIC4 I (accommodation, food) -> TRH.
These shift small employment shares between sectors; the size of the shift
cannot be measured with the data at hand and is logged as an open question.
"""
import re

ISIC4 = {
    "A": "AGR", "B": "MIU", "C": "MAN", "D": "MIU", "E": "MIU", "F": "CON",
    "G": "TRH", "I": "TRH", "H": "TSC", "J": "TSC",
    **{k: "OTH" for k in "KLMNOPQRSTU"},
}
ISIC3 = {
    "A": "AGR", "B": "AGR", "C": "MIU", "D": "MAN", "E": "MIU", "F": "CON",
    "G": "TRH", "H": "TRH", "I": "TSC",
    **{k: "OTH" for k in "JKLMNOPQ"},
}
ISIC2 = {  # major divisions
    "1": "AGR", "2": "MIU", "3": "MAN", "4": "MIU", "5": "CON",
    "6": "TRH", "7": "TSC", "8": "OTH", "9": "OTH",
}

# Scheme preference when a country-year has more than one breakdown.
SCHEME_RANK = {"ISIC4": 0, "DETAILS": 1, "ISIC3": 2, "ISIC2": 3}


def map_ilo_code(code: str):
    """Return (scheme, kind, sector) for an ILO classif1 code.

    kind is 'total', 'x' (not classified), 'detail' (maps to one target
    sector), 'mixed' (spans several target sectors, unusable) or 'other'
    (a scheme we do not use, e.g. ECO_SECTOR / ECO_AGGREGATE).
    """
    m = re.match(r"^ECO_(ISIC4|ISIC3|ISIC2|DETAILS)_(.+)$", str(code))
    if not m:
        return (None, "other", None)
    scheme, tail = m.groups()
    if tail == "TOTAL":
        return (scheme, "total", None)
    if tail == "X":
        return (scheme, "x", None)
    table = {"ISIC4": ISIC4, "DETAILS": ISIC4, "ISIC3": ISIC3, "ISIC2": ISIC2}[scheme]
    # ISIC2 tails are digits; others are one or more ISIC letters (e.g. 'MN', 'RSTU').
    parts = list(tail) if scheme != "ISIC2" else [tail[0]]
    if scheme == "ISIC2" and tail == "0":
        return (scheme, "x", None)
    sectors = {table.get(p) for p in parts}
    if None in sectors:
        return (scheme, "unknown", None)
    if len(sectors) > 1:
        return (scheme, "mixed", None)
    return (scheme, "detail", sectors.pop())


# UN AMA indicator names (matched on the ISIC tag in brackets).
UN_INDICATORS = {
    "ISIC A-B": "AGR",
    "ISIC C-E": "_CDE",   # mining + manufacturing + utilities, used to derive MIU
    "ISIC D": "MAN",
    "ISIC F": "CON",
    "ISIC G-H": "TRH",
    "ISIC I": "TSC",
    "ISIC J-P": "OTH",
}


def map_un_indicator(name: str):
    """Return the target code for a UN AMA indicator name, 'TOTAL_VA', 'GDP' or None."""
    s = str(name).strip()
    m = re.search(r"\((ISIC [A-Z](?:-[A-Z])?)\)", s)
    if m:
        return UN_INDICATORS.get(m.group(1))
    low = s.lower()
    if low.startswith("total value added"):
        return "TOTAL_VA"
    if low.startswith("gross domestic product"):
        return "GDP"
    return None
