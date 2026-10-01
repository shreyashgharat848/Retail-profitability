"""Creates a SIMULATED category-level table for FreshBasket (Year 2)."""
import os, pandas as pd
cat = pd.DataFrame({
    "Category":      ["Staples","Fresh produce","Dairy","FMCG","Private label","Non-food"],
    "SalesShare%":   [24, 16, 12, 30, 8, 10],
    "GrossMargin%":  [10, 22, 12, 17, 30, 26],
    "Wastage%ofSales":[0.8, 6.0, 1.5, 0.6, 0.5, 0.4],
})
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "freshbasket_categories.csv")
cat.to_csv(out, index=False)
print(cat)
