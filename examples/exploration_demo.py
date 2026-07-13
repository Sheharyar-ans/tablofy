"""Tablofy exploration demo.

Demonstrates all data exploration methods with a sample dataset.
Run with: python examples/exploration_demo.py
"""

import pandas as pd

import tablofy as tf

df = pd.DataFrame({
    "customer":   ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank"],
    "age":        [25, 30, 35, None, 29, 42],
    "salary":     [50000.0, 60000.0, 70000.0, 80000.0, None, 95000.0],
    "department": ["Sales", "Eng", "Sales", "Eng", "HR", "Eng"],
    "start_date": pd.to_datetime([
        "2020-01-15", "2019-06-01", "2021-03-20",
        "2018-11-01", "2022-07-04", "2020-09-15",
    ]),
    "active": [True, False, True, True, False, True],
})

data = tf.TablofyFrame(df, name="employees")

print("=== preview() ===")
print(data.preview())

print("\n=== shape() ===")
s = data.shape()
print(f"  {s['rows']} rows x {s['columns']} columns")

print("\n=== columns() ===")
for col in data.columns():
    print(f"  - {col}")

print("\n=== types() ===")
print(data.types().to_string(index=False))

print("\n=== missing() ===")
miss = data.missing()
if len(miss):
    print(miss.to_string(index=False))
else:
    print("  No missing values.")

print("\n=== duplicates() ===")
d = data.duplicates()
print(f"  {d['count']} duplicate(s) ({d['percent']}%)")

print("\n=== summary() ===")
print(data.summary().to_string())

print("\n=== profile() ===")
p = data.profile()
for key, val in p.items():
    print(f"  {key}: {val}")

print("\nExploration demo completed successfully.")
