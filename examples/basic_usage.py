"""Basic Tablofy usage example.

Creates sample data in memory and demonstrates the core workflow.
Run with: python examples/basic_usage.py
"""

import pandas as pd

import tablofy as tf

# Create sample data
df = pd.DataFrame({
    "product":  ["Widget A", "Widget B", "Widget C", "Widget D", "Widget E"],
    "category": ["Tools", "Tools", "Garden", "Garden", "Tools"],
    "price":    [9.99, 14.99, 24.99, 5.99, 19.99],
    "stock":    [42, 108, 23, 67, 0],
})

data = tf.TablofyFrame(df, name="products")

print(f"Loaded: {data}")

# Inspect
print(f"\nShape: {data.shape()}")
print(f"Columns: {data.columns()}")

print("\nColumn types:")
for col, dtype in data.dtypes.items():
    print(f"  {col}: {dtype}")

print(f"\nFirst 3 rows:\n{data.head(3)}")

# Summary stats
print(f"\nSummary:\n{data.summary()}")

# Profile
p = data.profile()
print(f"\nProfile: {p['rows']} rows, {p['columns']} cols, "
      f"{p['numeric_columns']} numeric, {p['text_columns']} text")

# Export to pandas
pdf = data.to_pandas()
print(f"\nMax price via pandas: ${pdf['price'].max():.2f}")

# Column validation (error example)
try:
    data.select("nonexistent")
except tf.TablofyColumnError as e:
    print(f"\nColumn validation works: {e}")

print("\nBasic usage example completed successfully.")
