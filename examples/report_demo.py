"""Demonstration of HTML and Excel report generation.

Run with: python examples/report_demo.py
"""

from pathlib import Path

import pandas as pd

import tablofy as tf

out = Path("report_output")
out.mkdir(exist_ok=True)

data = tf.TablofyFrame(
    pd.DataFrame({
        "month": ["Jan", "Feb", "Mar", "Apr"],
        "sales": [100, 200, 150, 300],
        "profit": [30, 50, 40, 80],
        "city": ["NYC", "LA", "NYC", "LA"],
    }),
    name="quarterly",
)

# Clean before reporting
data.clean()

# HTML report
html_path = data.report(str(out / "report.html"))
print(f"HTML report: {html_path}")

# Excel report
xlsx_path = data.report(str(out / "report.xlsx"))
print(f"Excel report: {xlsx_path}")

# Report with charts
data.bar(x="month", y="sales", save=str(out / "chart.png"))
html_with_charts = data.report(
    str(out / "report_with_charts.html"),
    charts=[("Sales by Month", str(out / "chart.png"))],
)
print(f"HTML report (with charts): {html_with_charts}")

print("\nReport demo completed successfully.")
