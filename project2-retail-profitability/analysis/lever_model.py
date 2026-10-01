"""Lever impact sizing. Edit the ASSUMPTIONS and run. Uses Year 2 totals from the dataset."""
import os, pandas as pd
here = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(here, "..", "data", "freshbasket_outlets.csv"))
y2 = df[df.Year == "Y2"]
sales = y2.Sales.sum(); profit = y2.NetProfit.sum()
cogs = sales - y2.GrossProfit.sum()

# ---- ASSUMPTIONS (justify each one in your deck) ----
cogs_saving_pct   = 0.010   # 1% COGS reduction via vendor renegotiation (on top vendors ~60% of COGS)
vendor_coverage   = 0.60
wastage_cut_pct   = 0.25    # 25% reduction in wastage
pl_share_now, pl_share_target = 0.08, 0.14
pl_margin_uplift  = 0.10    # private label earns +10 pts margin vs branded
manpower_saving   = 0.05    # 5% via footfall-based scheduling
y2out = y2.groupby("Outlet").NetProfit.sum().sort_values().head(3).index
bottom = y2[y2.Outlet.isin(y2out)]
rent_cut_pct      = 0.15    # rent renegotiation on 3 weakest outlets

levers = {
  "Procurement renegotiation": cogs * cogs_saving_pct * vendor_coverage,
  "Wastage reduction":         y2.Wastage.sum() * wastage_cut_pct,
  "Private label push":        sales * (pl_share_target - pl_share_now) * pl_margin_uplift,
  "Manpower scheduling":       y2.Manpower.sum() * manpower_saving,
  "Fix bottom-3 outlets (rent)": bottom.Rent.sum() * rent_cut_pct,
}
out = pd.DataFrame({"Impact_Rs_Cr": [v/1e7 for v in levers.values()]}, index=levers.keys())
out["Margin_pts"] = [v/sales*100 for v in levers.values()]
out["Effort(1-5)"] = [3, 2, 4, 2, 4]   # your judgement; used for the impact-effort matrix
print(out.round(2))
print(f"\nTotal: Rs {out.Impact_Rs_Cr.sum():.2f} Cr = {out.Margin_pts.sum():.2f} margin pts")
print(f"Margin now {profit/sales*100:.2f}% -> {(profit+sum(levers.values()))/sales*100:.2f}%")
out.to_csv(os.path.join(here, "..", "data", "lever_impact.csv"))
