# Project 2: Profitability Improvement for a Regional Supermarket Chain

> **Disclaimer:** "FreshBasket" is a hypothetical client. All data is **simulated** (`analysis/generate_data.py`) and calibrated on public grocery-retail benchmarks (gross margin, rent and manpower as % of sales from DMart / Spencer's annual reports). Results demonstrate the method, not real company performance.

## Problem statement
FreshBasket runs 36 supermarkets across Telangana and Andhra Pradesh. Net margin fell from about **7% to about 4%** over two years. **Why, and how can it be recovered?**

## Approach
1. **Profit tree:** Profit = Revenue (footfall x conversion x basket) minus costs (COGS, wastage, manpower, rent, utilities, other).
2. **Margin bridge (waterfall):** Year 1 to Year 2, split by cost line.
3. **Outlet diagnostic:** quartile ranking, Pareto (80/20) of profit, sales per sq ft vs margin, cuts by city and store size.
4. **Category view:** share of sales vs share of gross profit; wastage hotspots (fresh produce).
5. **Lever sizing:** procurement, wastage, private label, manpower scheduling, bottom-outlet fixes, each in Rs Cr and margin points.
6. **Prioritisation:** impact vs effort 2x2; 12-month roadmap with KPIs.

## Folder guide
| Path | Contents |
|---|---|
| `analysis/generate_data.py` | Creates `data/freshbasket_outlets.csv` (36 outlets x 24 months) |
| `analysis/generate_categories.py` | Creates `data/freshbasket_categories.csv` |
| `analysis/analysis.py` | Margin bridge, Pareto, scatter, outlet ranking (saves charts to `charts/`) |
| `analysis/lever_model.py` | Lever impact sizing (edit assumptions, run) |
| `excel/` | Pivot tables, lever model workbook |
| `deck/` | 10-12 slide deck |

## How to run (in this order)
```bash
pip install -r ../requirements.txt
cd analysis
python generate_data.py
python generate_categories.py
python analysis.py
python lever_model.py
```

## Results from the included run (seed 42)
- Net margin: **7.1% (Y1) to 3.8% (Y2)**
- Biggest driver: gross margin compression (about -1.5 pts), then manpower (-0.7), wastage (-0.5) and rent (-0.5)
- 20 of 36 outlets generate 80% of profit; 2 outlets are loss-making in Year 2
- Hyderabad outlets have the lowest margin (about 2.3%) because of higher rent
- Levers sized at about **Rs 4.0 Cr, or about 2 margin points** (0.5 wastage, 0.5 procurement, 0.6 private label, 0.3 manpower, 0.1 outlet fixes)

If you change the seed or parameters, update these numbers with your own output.

## Recommendation
Start with quick wins (wastage control, shift scheduling) in 0-3 months, then procurement renegotiation and private label expansion in 3-9 months, and decide on rent renegotiation or exit for the weakest outlets in 9-12 months. Track net margin, wastage %, sales per sq ft and gross margin by category monthly.

## Tools
Python (pandas, matplotlib), Excel, PowerPoint
