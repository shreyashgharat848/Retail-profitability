"""Generates a SIMULATED outlet-level P&L dataset for FreshBasket (36 outlets x 24 months).
Calibrated so net margin is roughly 7% in Year 1 and 4% in Year 2. Not real client data."""
import os
import numpy as np, pandas as pd
np.random.seed(42)

outlets = [f"O{str(i).zfill(2)}" for i in range(1, 37)]
cities = np.random.choice(["Hyderabad","Warangal","Vijayawada","Guntur","Karimnagar"], 36,
                          p=[.4,.15,.2,.15,.1])
size = np.random.choice([3000,5000,8000], 36, p=[.3,.5,.2])      # sq ft
rent_psf = np.where(cities == "Hyderabad", 60, 38)               # Rs/sqft/month

rows = []
for o, c, s, r in zip(outlets, cities, size, rent_psf):
    base_sales = s * np.random.uniform(820, 1250)                 # monthly sales (Rs)
    staff_cost = s / 200 * 12000                                 # ~1 staff per 100 sqft
    for m in range(24):
        y2 = m >= 12
        sales = base_sales * (1 + np.random.normal(0, .05)) * (0.96 if y2 else 1)
        gm = np.random.normal(0.215 if not y2 else 0.200, .008)  # gross margin compression
        gp = sales * gm
        wastage = sales * np.random.uniform(.012, .018) * (1.35 if y2 else 1)
        manpower = staff_cost * (1.07 if y2 else 1)
        rent = s * r * (1.06 if y2 else 1)
        utilities = s * np.random.uniform(5, 7) * (1.05 if y2 else 1)
        other = sales * 0.012
        profit = gp - wastage - manpower - rent - utilities - other
        rows.append([o, c, s, m + 1, "Y2" if y2 else "Y1", sales, gp, wastage,
                     manpower, rent, utilities, other, profit])

df = pd.DataFrame(rows, columns=["Outlet","City","SqFt","Month","Year","Sales","GrossProfit",
    "Wastage","Manpower","Rent","Utilities","Other","NetProfit"])
df["NetMargin%"] = df.NetProfit / df.Sales * 100

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "freshbasket_outlets.csv")
df.to_csv(out, index=False)

# Sanity check
g = df.groupby("Year")[["Sales","NetProfit"]].sum()
print((g.NetProfit / g.Sales * 100).round(2))
print("Loss-making outlets (Y2):",
      (df[df.Year=="Y2"].groupby("Outlet").NetProfit.sum() < 0).sum())
