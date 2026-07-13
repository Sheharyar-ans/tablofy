"""Demonstration of Tablofy charting operations.

Run with: python examples/charts_demo.py
"""

from pathlib import Path

import pandas as pd

import tablofy as tf

data = tf.TablofyFrame(
    pd.DataFrame({
        "month": ["Jan", "Feb", "Mar", "Apr", "May"],
        "sales": [100, 200, 150, 300, 250],
        "profit": [30, 50, 40, 80, 65],
        "ad_spend": [10, 25, 15, 35, 28],
    }),
    name="sales_data",
)

out = Path("charts_output")
out.mkdir(exist_ok=True)

# Standard charts (saved to file)
data.bar(x="month", y="sales", save=str(out / "bar.png"))
print("Saved bar.png")

data.line(x="month", y="sales", save=str(out / "line.png"))
print("Saved line.png")

data.scatter(x="ad_spend", y="sales", save=str(out / "scatter.png"))
print("Saved scatter.png")

data.hist("sales", save=str(out / "hist.png"))
print("Saved hist.png")

data.box(x="month", y="sales", save=str(out / "box.png"))
print("Saved box.png")

data.heatmap(save=str(out / "heatmap.png"))
print("Saved heatmap.png")

# Pairplot (shown but not saved automatically)
data.pairplot()
print("Pairplot displayed (not saved)")

# Smart chart (plain English)
fig = data.chart("sales by month")
fig.savefig(str(out / "smart_bar.png"))
print("Saved smart_bar.png (from 'sales by month')")

fig2 = data.chart("profit vs ad_spend")
fig2.savefig(str(out / "smart_scatter.png"))
print("Saved smart_scatter.png (from 'profit vs ad_spend')")

print(f"\nAll charts saved to {out.resolve()}/")
print("Charts demo completed successfully.")
