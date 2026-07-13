# Quick Start

This guide walks through loading, cleaning, exploring, charting, and reporting — all with Tablofy.

## 1. Install

```bash
pip install tablofy
```

## 2. Load data

```python
import tablofy as tf

data = tf.load("sales.csv")
```

Supports CSV, Excel (`.xlsx` / `.xls`), JSON, and Parquet.

## 3. Take a quick look

```python
print(data.preview())     # first 5 rows
print(data.shape())       # {"rows": 100, "columns": 8}
print(data.columns())     # ["date", "region", "product", ...]
print(data.profile())     # full dataset profile
```

## 4. Clean

```python
data.clean()
```

This one call:

- Removes duplicate rows
- Fills missing numbers with median, missing text with mode
- Converts column names to `snake_case`
- Strips whitespace from text values
- Tries to parse date columns

```python
# See what was cleaned
print(data.clean_report()["summary_text"])
```

## 5. Explore

```python
print(data.summary())     # mean, std, min, max, etc.
print(data.missing())     # columns with null values
print(data.duplicates())  # duplicate row stats
print(data.types())       # dtypes of every column
```

## 6. Chart

```python
data.bar(x="region", y="sales")
data.line(x="date", y="sales")
data.scatter(x="ads", y="sales")
data.hist("price")
data.box(x="region", y="sales")
```

Or use plain English:

```python
data.chart("sales by region")          # bar chart
data.chart("profit vs ad_spend")       # scatter plot
```

Save any chart:

```python
data.bar(x="region", y="sales", save="chart.png")
```

## 7. Detect issues automatically

```python
for insight in data.insights():
    print(f"  - {insight}")
```

Rule-based observations about missing values, duplicates, correlations, and outliers.

## 8. Run SQL

```python
result = data.sql("SELECT region, SUM(sales) AS total FROM data GROUP BY region")
print(result.preview())
```

The table name is always `data`. The result is a `TablofyFrame` so you can chain.

## 9. Generate a report

```python
data.report("report.html")    # self-contained HTML page
data.report("report.xlsx")    # multi-sheet Excel workbook
```

## Full example

```python
import tablofy as tf

data = tf.load("sales.csv")
data.clean()

print(data.profile())
data.chart("sales by region")
data.report("report.html")

for insight in data.insights():
    print(f"  - {insight}")
```
