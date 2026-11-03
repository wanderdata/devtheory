# trapmodel changelog

Versioning: MAJOR changes the economic structure in a way that changes conclusions; MINOR adds a mechanism or parameter; PATCH changes calibration, fixes or code only. Every version bump reruns `pytest` and `experiments.py`.

## 0.1.0 — 2026-11-03

First version, built for WP04.

**Structure.** Three segments (modern tradable, modern non-tradable, traditional). Managers are the binding factor for modern firms. Two goods; the real exchange rate clears the non-tradable market. A payroll-financed state with transfers to informal workers. Commodity rents, foreign ownership and saving abroad. Capability (K) and relative productivity (A) dynamics. Six switchable mechanisms. Scenarios: baseline, lac_type, escaper, resource_rich_advanced, boom_ratchet.

**Design decisions taken while building (all logged as D-015):**
1. *Spending scaled to income, not fixed amounts.* With fixed levels, the wedge sat at its ceiling everywhere and the fiscal loop was inert.
2. *Transfers indexed per informal worker to average income.* With spending as a fixed share of GDP, the informal sector's value moved one-for-one with formal income (Cobb–Douglas demand), so the "narrow base" never bit. Non-contributory transfers per beneficiary tied to average income reproduce the loop.
3. *Spending indexed to non-resource GDP.* Indexing to total GDP made commodity booms raise payroll-financed transfers mechanically. That exaggerated the ratchet: even a boom 70% saved abroad tipped the economy.
4. *`kappa_R` added.* It sets whether the state's rent revenue cuts the wedge (relief) or funds extra spending (procyclical). With full relief, booms helped rather than hurt.
5. *Budget surplus closure.* If rents exceed needs and the wedge is zero, the surplus is spent publicly.

**Known limitations.**
- The trap's multiplicity comes mainly from the fiscal loop (WP04 §5).
- The absorption constraint (framework Idea 5) is weak.
- There are no balance-of-payments crises (trade balances every period).
- Transitions are fast because static equilibrium adjusts instantly.
