"""Demonstration of SQL query support.

Run with: python examples/sql_demo.py
"""

import pandas as pd

import tablofy as tf

data = tf.TablofyFrame(
    pd.DataFrame({
        "name": ["Alice", "Bob", "Charlie", "Diana"],
        "sales": [100, 200, 150, 300],
        "region": ["North", "South", "North", "South"],
    }),
    name="sales_data",
)

# Simple SELECT
print("=== All rows ===")
print(data.sql("SELECT * FROM data").preview())

# Filtered
print("\n=== Sales > 150 ===")
print(data.sql("SELECT * FROM data WHERE sales > 150").preview())

# Aggregation
print("\n=== Total sales by region ===")
result = data.sql(
    "SELECT region, SUM(sales) AS total FROM data GROUP BY region"
)
print(result.preview())

# Sorted
print("\n=== Sorted by sales (descending) ===")
print(data.sql("SELECT * FROM data ORDER BY sales DESC").preview())

# Chaining with TablofyFrame methods
print("\n=== Chained: SQL -> select -> sort ===")
chained = (
    data.sql("SELECT * FROM data WHERE sales > 100")
    .select("name", "sales")
    .sort("sales", descending=True)
)
print(chained.preview())

print("\nSQL demo completed successfully.")
