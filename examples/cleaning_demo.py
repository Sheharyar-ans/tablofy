"""Tablofy cleaning demo.

Demonstrates data cleaning, smart missing-value filling, column name
normalisation, and the cleaning report.
Run with: python examples/cleaning_demo.py
"""

import pandas as pd

import tablofy as tf

# Create a deliberately messy dataset
df = pd.DataFrame({
    "  First Name  ": ["  Alice  ", "  Bob  ", "Charlie", "  Diana  ", "  Eve  "],
    "AGE ": [25, None, 35, None, 29],
    "SALARY ": [50000.0, 60000.0, None, 80000.0, 65000.0],
    "empty_col": [None, None, None, None, None],
    "NOTES": ["hello", "world", None, "hello", "world"],
    "Start Date": ["2020-01-15", "2019-06-01", "2021-03-20", "not-a-date", "2022-07-04"],
})

data = tf.TablofyFrame(df, name="employees")

print("=" * 60)
print("BEFORE CLEANING")
print("=" * 60)
print(f"Shape: {data.shape()}")
print(f"Columns: {data.columns()}")
print(f"\nData preview:\n{data.preview()}")
print(f"\nMissing:\n{data.missing().to_string(index=False)}")
print(f"\nDuplicates: {data.duplicates()}")

# Clean
data.clean()

print("\n" + "=" * 60)
print("AFTER CLEANING")
print("=" * 60)
print(f"Shape: {data.shape()}")
print(f"Columns: {data.columns()}")
print(f"\nData preview:\n{data.preview()}")
print(f"\nMissing:\n{data.missing().to_string(index=False)}")

# Cleaning report
print("\n" + "=" * 60)
print("CLEANING REPORT")
print("=" * 60)
report = data.clean_report()
print(report["summary_text"])
for action in report["actions"]:
    print(f"  - [{action['action']}] {action['message']}")

# Chaining demo
print("\n" + "=" * 60)
print("CHAINING: data.clean().summary()")
print("=" * 60)
summary = data.clean().summary()
print(summary.to_string())

print("\nCleaning demo completed successfully.")
