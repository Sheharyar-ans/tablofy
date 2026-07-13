"""Tablofy quickstart example.

Run with: python examples/quickstart.py
"""

import pandas as pd

import tablofy as tf

data = tf.TablofyFrame(
    pd.DataFrame({
        "name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
        "age": [25, 30, 35, 40, None],
        "salary": [50000, 60000, 70000, 80000, 65000],
        "department": ["Sales", "Eng", "Sales", "Eng", "HR"],
    }),
    name="Employees",
)

# --- Inspect ---
print("Shape:", data.shape())
print("Columns:", data.columns())
print("Types:")
print(data.types())

# --- Clean ---
data.clean()
print("\nAfter clean — missing age count:", data._df["age"].isna().sum())

# --- Profile ---
prof = data.profile()
print(f"\nProfile — rows: {prof['rows']}, cols: {prof['columns']}")
print(f"  Numeric: {prof['numeric_columns']}")
print(f"  Text: {prof['text_columns']}")

# --- Chart (saves to file) ---
fig = data.hist("age")
fig.savefig("histogram_age.png")
print("\nSaved histogram_age.png")

fig2 = data.scatter(x="age", y="salary")
fig2.savefig("scatter_age_salary.png")
print("Saved scatter_age_salary.png")

# --- Insights ---
print("\nInsights:")
for obs in data.insights():
    print(f"  - {obs}")

# --- Report ---
data.report("employees_report.html")
print("Saved employees_report.html")
