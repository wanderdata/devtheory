"""
WP03 - Where does US$100 of a firm's value added go, by ownership and market?

ILLUSTRATIVE parameters. Every firm generates the same US$100 of value added:
wages 35, taxes 15, gross profits 50 (before any royalty/fee or profit shifting).
What changes across cases is who owns the profits, how much leaves as royalties/
fees/transfer prices, what share is reinvested at home, and whether the firm sells
abroad (earning foreign exchange) or at home (not earning it).

Run:  python3 rent_leakage.py  -> prints table, writes rent_leakage.csv
"""
import csv
from pathlib import Path

VA, WAGES, TAXES, PROFITS = 100.0, 35.0, 15.0, 50.0
MPC_WAGES, M_WAGES = 0.90, 0.25          # consumption propensity and import share of workers' consumption
MPC_OWNERS, M_OWNERS = 0.50, 0.45        # domestic owners' consumption propensity (of distributed, not-offshored profit) and import share
M_INVEST = 0.40                          # import share of investment spending (machinery)
TAX_ON_SHIFTED = 0.0                     # shifted profit escapes host-country tax

CASES = {
    # fee: royalties/fees/transfer-price outflow taken from profits before host tax base
    # foreign: profits owned abroad; reinv: share of remaining profit reinvested at home
    # offshore: share of domestic owners' remaining profit sent abroad (capital flight)
    # export: share of output sold abroad (earns FX)
    "Foreign brand, sells at home (beverage-type)":      dict(fee=15, foreign=True,  reinv=0.40, offshore=0.0, export=0.0),
    "Foreign firm, exports (assembly/mining-type)":      dict(fee=5,  foreign=True,  reinv=0.40, offshore=0.0, export=1.0),
    "Foreign firm, profit shifting via transfer prices": dict(fee=30, foreign=True,  reinv=0.20, offshore=0.0, export=0.0),
    "Domestic firm, owners reinvest at home":            dict(fee=0,  foreign=False, reinv=0.60, offshore=0.0, export=0.0),
    "Domestic firm, owners move savings offshore":       dict(fee=0,  foreign=False, reinv=0.20, offshore=0.50, export=0.0),
}


def flows(c):
    fee = c["fee"]
    # profit shifting lowers the taxable base; here only the explicit 'profit shifting' case loses tax
    tax_loss = 0.25 * (fee - 15) if fee > 15 else 0.0     # extra fees beyond a normal brand royalty erode taxes
    taxes = TAXES - tax_loss
    profit = PROFITS - fee + tax_loss                      # identity: wages + taxes + fee + profit = VA
    reinvested = c["reinv"] * profit
    if c["foreign"]:
        repatriated = profit - reinvested
        owners_spend_dom = 0.0
        offshore = 0.0
    else:
        repatriated = 0.0
        distributed = profit - reinvested
        offshore = c["offshore"] * distributed
        owners_spend_dom = MPC_OWNERS * (distributed - offshore) * (1 - M_OWNERS)
    foreign_claims_paid = fee + repatriated                # cash leaving to foreign owners/affiliates now
    national_income = VA - fee - (profit if c["foreign"] else 0.0)  # GNI view: foreign-owned profit (incl. reinvested) is foreign income
    wages_spend_dom = MPC_WAGES * WAGES * (1 - M_WAGES)
    invest_spend_dom = reinvested * (1 - M_INVEST)
    first_round_dom_demand = wages_spend_dom + owners_spend_dom + invest_spend_dom
    fx_earned = c["export"] * VA                           # simplification: exported value added
    fx_needed = foreign_claims_paid + offshore + M_INVEST * reinvested
    return dict(
        taxes=taxes, fees_abroad=fee, profits_repatriated=repatriated, reinvested_at_home=reinvested,
        domestic_capital_flight=offshore, national_income=national_income,
        first_round_domestic_demand=first_round_dom_demand, net_FX=fx_earned - fx_needed,
    )


def main():
    for k, c in CASES.items():
        f = flows(c)
        # accounting check: value added = wages + taxes + fees + after-fee profit
        profit = VA - WAGES - f["taxes"] - f["fees_abroad"]
        assert profit >= 0, k
        if c["foreign"]:   # foreign profit is either repatriated or reinvested
            assert abs(f["profits_repatriated"] + f["reinvested_at_home"] - profit) < 1e-9, k
        else:              # domestic profit: reinvested + distributed (of which some offshored)
            assert f["reinvested_at_home"] <= profit and f["domestic_capital_flight"] <= profit - f["reinvested_at_home"], k
    rows = [{"case": k, **{kk: round(v, 1) for kk, v in flows(c).items()}} for k, c in CASES.items()]
    out = Path(__file__).with_name("rent_leakage.csv")
    with out.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(" | ".join(rows[0].keys()))
    for r in rows:
        print(" | ".join(str(v) for v in r.values()))


if __name__ == "__main__":
    main()
