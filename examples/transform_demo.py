"""Demonstration of Tablofy transformation operations.

Run with: python examples/transform_demo.py
"""

import pandas as pd

import tablofy as tf

data = tf.TablofyFrame(
    pd.DataFrame({
        "name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
        "age": [25, 30, 35, 28, 32],
        "salary": [50000, 60000, 70000, 80000, 65000],
        "region": ["North", "South", "North", "South", "North"],
    }),
    name="employees",
)

print(f"Loaded: {data}")
print(data.preview())

# Select + Filter
result = data.select("name", "region", "salary").filter("region == 'North'")
print("\n--- North region (name, region, salary) ---")
print(result.preview())

# Group By
grouped = data.group("region").sum("salary")
print("\n--- Total salary by region ---")
print(grouped.preview())

# Sort
sorted_df = data.sort("salary", descending=True)
print("\n--- Sorted by salary (descending) ---")
print(sorted_df.preview())

# Pivot
pivoted = data.pivot(index="region", columns="name", values="salary", aggfunc="sum")
print("\n--- Pivot: salary by region x name ---")
print(pivoted.preview())

# Chained pipeline
pipeline = (
    data
    .drop("age")
    .rename({"name": "full_name"})
    .sort("salary", descending=True)
)
print("\n--- Chained pipeline: drop -> rename -> sort ---")
print(pipeline.preview())
print(f"Columns: {pipeline.columns()}")

print("\nTransform demo completed successfully.")
