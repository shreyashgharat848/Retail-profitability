"""Starter analysis for Project 2. Run generate_data.py first.
Produces: margin bridge (waterfall), Pareto, scatter, outlet ranking."""
import os
import pandas as pd, numpy as np
import matplotlib.pyplot as plt

here = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(here, "..", "data", "freshbasket_outlets.csv"))
os.makedirs(os.path.join(here, "..", "charts"), exist_ok=True)
def save(name): plt.tight_layout(); plt.savefig(os.path.join(here, "..", "charts", name), dpi=150); plt.close()

# 1) Margin bridge Y1 -> Y2 (each cost as % of sales)
cols = ["GrossProfit","Wastage","Manpower","Rent","Utilities","Other"]
tot = df.groupby("Year")[cols + ["Sales","NetProfit"]].sum()
pct = tot[cols].div(tot["Sales"], axis=0) * 100
delta = pct.loc["Y2"] - pct.loc["Y1"]
steps = {"Gross margin": delta["GrossProfit"], "Wastage": -delta["Wastage"],
         "Manpower": -delta["Manpower"], "Rent": -delta["Rent"],
         "Utilities": -delta["Utilities"], "Other": -delta["Other"]}
start = tot.loc["Y1","NetProfit"] / tot.loc["Y1","Sales"] * 100
end = tot.loc["Y2","NetProfit"] / tot.loc["Y2","Sales"] * 100
labels = ["Y1 margin"] + list(steps) + ["Y2 margin"]
vals = [start] + list(steps.values())
fig, ax = plt.subplots(figsize=(9,4.5)); run = start
ax.bar(0, start, color="#2E7D32")
for i, v in enumerate(steps.values(), 1):
    ax.bar(i, v, bottom=run, color="#C62828" if v < 0 else "#2E7D32"); run += v
ax.bar(len(labels)-1, end, color="#1565C0")
ax.set_xticks(range(len(labels))); ax.set_xticklabels(labels, rotation=20)
ax.set_ylabel("Net margin (% of sales)"); ax.set_title("Net margin bridge: Year 1 to Year 2")
save("1_margin_bridge.png")
print(f"Net margin Y1 {start:.2f}% -> Y2 {end:.2f}%"); print(steps)

# 2) Outlet ranking and Pareto (Year 2)
y2 = df[df.Year == "Y2"].groupby(["Outlet","City","SqFt"]).agg(
    Sales=("Sales","sum"), Profit=("NetProfit","sum")).reset_index()
y2["Margin%"] = y2.Profit / y2.Sales * 100
y2["SalesPerSqFt"] = y2.Sales / y2.SqFt / 12
y2["Quartile"] = pd.qcut(y2["Margin%"], 4, labels=["Q4 (worst)","Q3","Q2","Q1 (best)"])
y2 = y2.sort_values("Profit", ascending=False)
y2["CumProfit%"] = y2.Profit.clip(lower=0).cumsum() / y2.Profit.clip(lower=0).sum() * 100
y2.to_csv(os.path.join(here, "..", "data", "outlet_ranking_y2.csv"), index=False)
n80 = (y2["CumProfit%"] < 80).sum() + 1
print(f"{n80} of {len(y2)} outlets generate 80% of profit; loss-making: {(y2.Profit<0).sum()}")

fig, ax = plt.subplots(figsize=(9,4.5))
ax.bar(range(len(y2)), y2.Profit/1e5, color="#1565C0"); ax.set_ylabel("Y2 profit (Rs lakh)")
ax2 = ax.twinx(); ax2.plot(range(len(y2)), y2["CumProfit%"], color="#E65100"); ax2.axhline(80, ls="--", c="grey")
ax.set_xticks(range(len(y2))); ax.set_xticklabels(y2.Outlet, rotation=90, fontsize=7)
ax.set_title("Pareto: outlet profit contribution (Year 2)")
save("2_pareto.png")

# 3) Scatter: sales per sq ft vs margin
fig, ax = plt.subplots(figsize=(7,5))
for city, g in y2.groupby("City"): ax.scatter(g.SalesPerSqFt, g["Margin%"], label=city)
ax.axhline(0, c="grey", lw=.8); ax.set_xlabel("Sales per sq ft per month (Rs)"); ax.set_ylabel("Net margin %")
ax.legend(); ax.set_title("Productivity vs margin by outlet")
save("3_scatter.png")

# 4) Segment views
print(y2.groupby("City")[["Sales","Profit"]].sum().assign(**{"Margin%": lambda d: d.Profit/d.Sales*100}).round(1))
print(y2.groupby("SqFt")[["Sales","Profit"]].sum().assign(**{"Margin%": lambda d: d.Profit/d.Sales*100}).round(1))
