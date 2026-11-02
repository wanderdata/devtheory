"""
WP01 - Worked examples for the three-ledger evaluation of firms.

Every firm has US$100m of sales. Parameters are ILLUSTRATIVE (stylized orders of
magnitude), except where the paper cites a source (maquila domestic value-added
share ~21%, Castillo & de Vries). Change them and re-run; the paper's table is
generated from this file.

Run:  python3 ledger_examples.py   -> prints table, writes ledger_examples.csv
"""
import csv
from pathlib import Path

SALES = 100.0          # US$ millions
IMPORT_CONTENT_DOMESTIC_INPUTS = 0.25   # import content embodied in domestic suppliers' output
Y_T = 5_000            # US$ value added per worker in the traditional (informal) segment = opportunity cost of labor
MPC_WAGES = 0.90       # marginal propensity to consume out of wages
MPC_PROFITS = 0.30     # out of domestically retained profits (rest saved/reinvested)
IMPORT_SHARE_CONS = {  # import share of the consumption basket of each income group
    "low_wage": 0.20, "high_wage": 0.40, "owners": 0.45,
}

# fields: imported inputs, domestic inputs, wages, profits, taxes, share of profits remitted abroad,
#         royalties/fees paid abroad, workers, export share, wage-earner type
FIRMS = {
    "Foreign copper mine":          dict(imp=15, dom=25, w=8,  p=35, t=17, remit=1.00, roy=2, L=80,   x=1.00, wtype="high_wage"),
    "Maquila electronics assembly": dict(imp=75, dom=8,  w=10, p=5,  t=2,  remit=1.00, roy=0, L=1000, x=1.00, wtype="low_wage"),
    "Domestic fruit agro-exporter": dict(imp=10, dom=30, w=30, p=25, t=5,  remit=0.00, roy=0, L=3000, x=0.90, wtype="low_wage"),
    "Domestic software/BPO exporter": dict(imp=10, dom=15, w=55, p=15, t=5, remit=0.00, roy=0, L=1100, x=1.00, wtype="high_wage"),
    "Domestic hotel (foreign guests)": dict(imp=15, dom=30, w=30, p=20, t=5, remit=0.00, roy=0, L=1500, x=1.00, wtype="low_wage"),
    "Modern supermarket chain":     dict(imp=35, dom=49, w=9,  p=5,  t=2,  remit=0.00, roy=0, L=900,  x=0.00, wtype="low_wage"),
    "Informal corner shops":        dict(imp=30, dom=55, w=15, p=0,  t=0,  remit=0.00, roy=0, L=3000, x=0.00, wtype="low_wage"),
}


def ledger(f):
    va_direct = f["w"] + f["p"] + f["t"]
    assert abs(f["imp"] + f["dom"] + va_direct - SALES) < 1e-9, "sales must equal inputs + value added"
    va_domestic_total = SALES - f["imp"] - IMPORT_CONTENT_DOMESTIC_INPUTS * f["dom"]  # direct + supplier VA
    remitted = f["remit"] * f["p"] + f["roy"]
    national_income = va_domestic_total - remitted                                    # GNI-type contribution
    imports_total = f["imp"] + IMPORT_CONTENT_DOMESTIC_INPUTS * f["dom"]
    net_fx = f["x"] * SALES - imports_total - remitted                                # net foreign exchange
    wage_spend_domestic = MPC_WAGES * f["w"] * (1 - IMPORT_SHARE_CONS[f["wtype"]])
    profit_spend_domestic = MPC_PROFITS * (1 - f["remit"]) * f["p"] * (1 - IMPORT_SHARE_CONS["owners"])
    first_round_demand = wage_spend_domestic + profit_spend_domestic
    va_per_worker = va_direct * 1e6 / f["L"]
    net_gain_vs_informal = va_direct - f["L"] * Y_T / 1e6                             # value added net of labor's opportunity cost
    return dict(
        direct_VA=va_direct, domestic_VA=va_domestic_total, national_income=national_income,
        net_FX=net_fx, local_demand_1st_round=first_round_demand, workers=f["L"],
        VA_per_worker_usd=va_per_worker, net_gain_vs_informal=net_gain_vs_informal,
    )


def main():
    rows = []
    for name, f in FIRMS.items():
        r = ledger(f)
        r = {"firm": name, **{k: round(v, 1) if isinstance(v, float) else v for k, v in r.items()}}
        rows.append(r)
    out = Path(__file__).with_name("ledger_examples.csv")
    with out.open("w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        wr.writeheader()
        wr.writerows(rows)
    cols = list(rows[0].keys())
    print(" | ".join(cols))
    for r in rows:
        print(" | ".join(str(r[c]) for c in cols))


if __name__ == "__main__":
    main()
