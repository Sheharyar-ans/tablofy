# Reports

Generate HTML or Excel reports from a `TablofyFrame` with one call.

```python
data.report("report.html")
data.report("report.xlsx")
```

## HTML Report

The HTML report is a self-contained page you can open in any browser.

### Sections

- **Dataset Overview** — rows, columns, missing cells, duplicates, column-type counts
- **Columns** — every column grouped by type (numeric, text, date, categorical)
- **Missing Values** — null count and percentage per column
- **Summary Statistics** — descriptive stats for all columns
- **Insights** — rule-based observations
- **Cleaning Report** — actions from the last `clean()` call, if any
- **Charts** — optional embedded chart images

### Embedding charts

```python
data.bar(x="month", y="sales", save="chart.png")
data.report("report.html", charts=[("Sales by Month", "chart.png")])
```

## Excel Report

Multi-sheet workbook with:

| Sheet | Contents |
|-------|----------|
| Data | Raw data |
| Summary | Descriptive statistics |
| Missing Values | Null count and percent per column |
| Insights | Rule-based observations |
| Cleaning Report | Actions from the last `clean()` |

## Supported formats

| Extension | Format |
|-----------|--------|
| `.html` | Self-contained HTML page |
| `.xlsx` | Multi-sheet Excel workbook |
