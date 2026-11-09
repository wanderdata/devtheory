"""Countries, names and ECLAC groupings shared by all pipelines and apps.

Single source of truth: pipelines (empirics/code/*) and dashboards (apps/*) import
from here instead of keeping their own lists.

Membership: the 33 Latin American and Caribbean member States of ECLAC
(https://www.cepal.org/en/about/member-states-and-associate-members, checked
2026-11-09; D-030). Caribbean (broad definition, D-019): the 16 member States
served by the ECLAC subregional headquarters in Port of Spain
(https://caribbean.eclac.org/about, checked 2026-11-05).
"""

# ISO3 -> (UN M49 numeric code, official ECLAC name, short name for charts)
COUNTRIES = {
    "ARG": (32, "Argentina", "Argentina"),
    "ATG": (28, "Antigua and Barbuda", "Antigua and Barbuda"),
    "BHS": (44, "Bahamas", "Bahamas"),
    "BLZ": (84, "Belize", "Belize"),
    "BOL": (68, "Bolivia (Plurinational State of)", "Bolivia (Plur. State of)"),
    "BRA": (76, "Brazil", "Brazil"),
    "BRB": (52, "Barbados", "Barbados"),
    "CHL": (152, "Chile", "Chile"),
    "COL": (170, "Colombia", "Colombia"),
    "CRI": (188, "Costa Rica", "Costa Rica"),
    "CUB": (192, "Cuba", "Cuba"),
    "DMA": (212, "Dominica", "Dominica"),
    "DOM": (214, "Dominican Republic", "Dominican Republic"),
    "ECU": (218, "Ecuador", "Ecuador"),
    "GRD": (308, "Grenada", "Grenada"),
    "GTM": (320, "Guatemala", "Guatemala"),
    "GUY": (328, "Guyana", "Guyana"),
    "HND": (340, "Honduras", "Honduras"),
    "HTI": (332, "Haiti", "Haiti"),
    "JAM": (388, "Jamaica", "Jamaica"),
    "KNA": (659, "Saint Kitts and Nevis", "Saint Kitts and Nevis"),
    "LCA": (662, "Saint Lucia", "Saint Lucia"),
    "MEX": (484, "Mexico", "Mexico"),
    "NIC": (558, "Nicaragua", "Nicaragua"),
    "PAN": (591, "Panama", "Panama"),
    "PER": (604, "Peru", "Peru"),
    "PRY": (600, "Paraguay", "Paraguay"),
    "SLV": (222, "El Salvador", "El Salvador"),
    "SUR": (740, "Suriname", "Suriname"),
    "TTO": (780, "Trinidad and Tobago", "Trinidad and Tobago"),
    "URY": (858, "Uruguay", "Uruguay"),
    "VCT": (670, "Saint Vincent and the Grenadines", "Saint Vincent and the Grenadines"),
    "VEN": (862, "Venezuela (Bolivarian Republic of)", "Venezuela (Bol. Rep. of)"),
}

LAC33 = sorted(COUNTRIES)
CARIBBEAN16 = ["ATG", "BHS", "BRB", "BLZ", "CUB", "DMA", "DOM", "GRD", "GUY", "HTI", "JAM",
               "KNA", "LCA", "VCT", "SUR", "TTO"]
LATIN_AMERICA_REST = [c for c in LAC33 if c not in CARIBBEAN16]   # the 17 not in the Caribbean scope

M49 = {iso: v[0] for iso, v in COUNTRIES.items()}
OFFICIAL = {iso: v[1] for iso, v in COUNTRIES.items()}
SHORT = {iso: v[2] for iso, v in COUNTRIES.items()}

# US$ levels not comparable for pooling (D-033): Venezuela (conversion at 2020 prices after
# hyperinflation), Cuba (official exchange rate).
POOL_EXCLUDE_LAC = ["CUB", "VEN"]

# Country scopes used by the productivity pipeline and app.
SCOPES = {
    "carib": dict(members=CARIBBEAN16, label="Caribbean", tag="carib_lp"),
    "lac": dict(members=LAC33, label="Latin America and the Caribbean", tag="lac_lp"),
}
