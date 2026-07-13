"""Demonstration of analytics: insights and statistics.

Run with: python examples/analytics_demo.py
"""

import pandas as pd

import tablofy as tf

data = tf.TablofyFrame(
    pd.DataFrame({
        "month": ["Jan", "Feb", "Mar", "Apr", "May"],
        "sales": [100, 200, 150, 300, 9999],
        "profit": [30, 50, 40, 80, 120],
        "ad_spend": [10, 25, 15, 35, 28],
    }),
    name="sales",
)

# Insights
print("=== Insights ===")
for note in data.insights():
    print(f"  - {note}")

# Stats
print("\n=== Describe ===")
print(data.stats.describe())

print("\n=== Correlation ===")
print(data.stats.correlation())

print("\n=== Covariance ===")
print(data.stats.covariance())

print("\n=== Outliers (sales) ===")
outliers = data.stats.outliers("sales")
print(outliers)

print("\n=== Outlier indices (sales) ===")
info = data.stats.outliers("sales", return_indices=True)
print(f"  Count: {info['count']}, Indices: {info['indices']}")

print("\n=== Univariate stats ===")
print(f"  Mean:  {data.stats.mean('sales')}")
print(f"  Min:   {data.stats.min('sales')}")
print(f"  Max:   {data.stats.max('sales')}")
print(f"  Std:   {data.stats.std('sales'):.2f}")

print("\nAnalytics demo completed successfully.")
