# Tablofy

A beginner-friendly data analytics library for Python. Tablofy is **not a pandas replacement** — it wraps pandas, matplotlib, seaborn, Plotly, and DuckDB under a simple, unified API so you can focus on analysis, not boilerplate.

```python
import tablofy as tf

data = tf.load("sales.csv")
data.clean()
print(data.profile())
data.chart("sales by month")
print(data.insights())
data.report("report.html")
```

## Installation

```bash
pip install tablofy
```

Requires Python 3.9 or later.

### Optional feature extras

Tablofy keeps its core lightweight. Install additional capabilities as needed:

| Command | Extras |
|---|---|
| `pip install tablofy[all]` | Everything below |
| `pip install tablofy[viz]` | Interactive Plotly charts |
| `pip install tablofy[ml]` | Scikit-learn machine learning helpers |
| `pip install tablofy[stats]` | SciPy / Statsmodels advanced statistics |
| `pip install tablofy[widgets]` | Jupyter Notebook interactive widgets |
| `pip install tablofy[scraping]` | Web scraping (BeautifulSoup, Requests) |
| `pip install tablofy[fast]` | Polars / PyArrow for large datasets |
| `pip install tablofy[dl]` | PyTorch / TensorFlow deep learning |

## Quick Start

```python
import tablofy as tf

# Load a CSV (also supports .xlsx, .json, .parquet)
data = tf.load("sales.csv")

# Explore
print(data.preview())        # first 5 rows
print(data.shape())          # {"rows": 100, "columns": 8}
print(data.profile())        # full dataset profile

# Clean in one go — duplicates, missing values, column names, dates
data.clean()

# Static chart (matplotlib / seaborn)
data.bar(x="region", y="sales")

# Interactive chart (requires: pip install tablofy[viz])
data.bar(x="region", y="sales", interactive=True)

# Plain-English chart descriptions
data.chart("sales by month")
data.chart("profit vs ad_spend")

# Automated insights
for note in data.insights():
    print(f"  - {note}")

# Run DuckDB SQL directly
print(data.sql("SELECT region, SUM(sales) FROM data GROUP BY region"))

# Generate a self-contained HTML report
data.report("report.html")
```

## Themes

Apply a consistent visual style to all charts — both static and interactive.

```python
tf.set_theme("dark")       # dark mode with neon accents
tf.set_theme("modern")     # clean, minimal, sans-serif
tf.set_theme("pastel")     # soft, bright colours
tf.set_theme("classic")    # academic, serif, no grid
tf.set_theme("modern", palette=["#ff6b6b", "#4ecdc4"])  # custom palette
```

Themes automatically affect matplotlib rcParams, seaborn palettes, and Plotly templates.

## Time-Series Helpers

```python
# Convert a column to datetime and set it as the index
data.ts.set_time_index("date")

# Resample to monthly totals
monthly = data.ts.resample(rule="ME", agg="sum")

# 7-day rolling average — adds a new column
data.ts.rolling(window=7, column="sales", agg="mean")

# Detect trend direction
data.ts.detect_trend("sales")
# → {"direction": "upward", "slope": 40.0, "strength": "strong"}
```

## Jupyter Notebook Widget Explorer

Inside a Jupyter notebook, launch an interactive dashboard with zero UI code:

```python
data.explore_interactive()
```

This renders a live widget panel with column selection, dynamic filters (sliders for numeric columns, multi-select for categories), an auto-updating table preview, and a chart that responds to every filter change.

Requires: `pip install tablofy[widgets]`

## Machine Learning Helpers

```python
# Requires: pip install tablofy[ml]
data.ml    # → MLWrapper with scikit-learn integration
```

Requires: `pip install tablofy[ml]`

## Web Scraping

```python
# Requires: pip install tablofy[scraping]
data.scrape    # → ScrapeWrapper with BeautifulSoup / Requests
```

Requires: `pip install tablofy[scraping]`

## Supported File Formats

| Extension | Format | Load | Export |
|-----------|--------|------|--------|
| `.csv` | Comma-separated values | `tf.load()` | `data.export()` |
| `.xlsx` | Excel workbook | `tf.load()` | `data.export()` |
| `.xls` | Excel 97–2003 | `tf.load()` | — |
| `.json` | JSON | `tf.load()` | `data.export()` |
| `.parquet` | Apache Parquet | `tf.load()` | `data.export()` |

## API Overview

### Loading

| Method | Description |
|--------|-------------|
| `tf.load(path)` | Load a file (auto-detects format) |
| `TablofyFrame(df, name)` | Wrap an existing pandas DataFrame |

### Exploration

| Method | Description |
|--------|-------------|
| `.preview(n=5)` | First *n* rows |
| `.head(n=5)` | Alias for preview |
| `.shape()` | Row and column counts (dict) |
| `.columns()` | Column names (list) |
| `.dtypes` | Column → dtype mapping (dict) |
| `.types()` | Column types and null counts (DataFrame) |
| `.missing()` | Columns with null values (DataFrame) |
| `.duplicates()` | Duplicate row stats (dict) |
| `.summary()` | Descriptive statistics (DataFrame) |
| `.profile()` | Full dataset profile (dict) |
| `.size` | Total cell count (int) |
| `len(data)` | Row count (int) |
| `.to_pandas()` | Get the underlying pandas DataFrame |

### Cleaning

| Method | Description |
|--------|-------------|
| `.clean()` | Clean in-place: duplicates, missing, column names, dates, whitespace |
| `.clean_report()` | Report of actions from last clean (dict) |

### Transform

| Method | Description |
|--------|-------------|
| `.select(*cols)` | New frame with only the given columns |
| `.drop(col)` | New frame without a column |
| `.rename(mapping)` | New frame with renamed columns |
| `.sort(by, descending)` | New frame sorted by a column |
| `.filter(expression)` | New frame filtered by a pandas query expression |
| `.group(by)` | A `GroupedFrame` for `.sum()` / `.mean()` aggregation |
| `.pivot(index, columns, values)` | Pivot table |
| `.join(other, on, how)` | Merge two frames on a shared key |
| `.export(path)` | Write to CSV, XLSX, JSON, or Parquet |

### Visualization

| Method | Description |
|--------|-------------|
| `.bar(x, y, interactive, save)` | Bar chart |
| `.line(x, y, interactive, save)` | Line chart |
| `.scatter(x, y, interactive, save)` | Scatter plot |
| `.hist(col, interactive, save)` | Histogram |
| `.box(x, y, interactive, save)` | Box plot |
| `.area(x, y, interactive, save)` | Area chart |
| `.pie(labels, values, interactive, save)` | Pie chart |
| `.violin(x, y, interactive, save)` | Violin plot |
| `.heatmap(interactive, save)` | Correlation heatmap |
| `.pairplot(save)` | Pairwise scatter matrix |
| `.chart(description)` | Smart chart from plain English |

All chart methods accept `interactive=True` to render an interactive Plotly chart (requires `tablofy[viz]`). Static charts use matplotlib / seaborn.

### Analytics

| Method | Description |
|--------|-------------|
| `.insights()` | Rule-based observations (list of strings) |
| `.stats.describe()` | Descriptive statistics (DataFrame) |
| `.stats.correlation()` | Correlation matrix (DataFrame) |
| `.stats.covariance()` | Covariance matrix (DataFrame) |
| `.stats.outliers(col)` | IQR outlier detection |
| `.stats.mean(col)` | Mean of a column |
| `.stats.median(col)` | Median of a column |
| `.stats.std(col)` | Standard deviation |
| `.stats.min(col)` | Minimum value |
| `.stats.max(col)` | Maximum value |
| `.stats.quantile(col, q)` | Quantile value |
| `.stats.value_counts(col)` | Frequency counts (Series) |

### Time Series

| Method | Description |
|--------|-------------|
| `.ts.set_time_index(col)` | Convert column to datetime index (in-place) |
| `.ts.resample(rule, agg)` | Resample by offset alias → new TablofyFrame |
| `.ts.rolling(window, col, agg)` | Rolling window statistic → new column |
| `.ts.detect_trend(col)` | Trend direction / slope / strength (dict) |

### SQL

| Method | Description |
|--------|-------------|
| `.sql(query)` | Run read-only SQL via DuckDB (table name: `data`) |

### Reports

| Method | Description |
|--------|-------------|
| `.report(path)` | Generate HTML or Excel report |

### Jupyter Integration

| Method | Description |
|--------|-------------|
| `.explore_interactive()` | Interactive widget dashboard (requires `tablofy[widgets]`) |
| `_repr_html_()` | Native HTML table rendering in notebooks |

## Examples

See the [`examples/`](examples/) directory for runnable scripts:

| Script | What it shows |
|--------|---------------|
| `basic_usage.py` | Core workflow: load → inspect → clean → chart |
| `exploration_demo.py` | All exploration methods |
| `cleaning_demo.py` | Cleaning pipeline + report |
| `transform_demo.py` | Select, filter, group, sort, pivot, chain |
| `charts_demo.py` | All chart types + smart chart |
| `analytics_demo.py` | Insights + statistics |
| `sql_demo.py` | SQL queries + chaining |
| `report_demo.py` | HTML + Excel reports |

## What Tablofy Is Not

- **Not a pandas replacement** — you can always access the underlying DataFrame with `.to_pandas()`
- **Not a big-data tool** — it operates in-memory on a single machine
- **Not a machine-learning framework** — it provides lightweight wrappers, not model training pipelines
- **Not a dashboard server** — reports are static HTML or Excel files
- **Not a database** — SQL runs in-memory against the loaded DataFrame only

## Contributing

Contributions are welcome! Open an issue or pull request on GitHub.

## License

MIT
