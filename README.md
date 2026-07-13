# Tablofy

A beginner-friendly data analytics library for Python. Tablofy is **not a pandas replacement** — it wraps pandas, matplotlib, seaborn, and DuckDB under a simple, unified API so you can focus on analysis, not boilerplate.

```python
import tablofy as tf

data = tf.load("sales.csv")
data.clean()
print(data.profile())
data.chart("sales by month")
print(data.insights())
data.report("report.html")
```

## What problem does Tablofy solve?

Pandas is powerful but has a steep learning curve. Tablofy wraps it so you can:

- **Load** CSV, Excel, JSON, and Parquet with a single function
- **Explore** your data with plain-English methods (`preview()`, `profile()`, `summary()`)
- **Clean** everything in one call (`clean()`) — duplicates, missing values, column names, dates, whitespace
- **Chart** without memorizing matplotlib or seaborn APIs
- **Run SQL** directly on a DataFrame using DuckDB
- **Report** with a single call to `report("report.html")`

No complex pandas syntax. No plotting boilerplate. No separate SQL database setup.

## Installation

```bash
pip install tablofy
```

Requires Python 3.9 or later.

## Quick Start

```python
import tablofy as tf

# Load a file
data = tf.load("sales.csv")

# Explore
print(data.preview())        # first 5 rows
print(data.shape())          # {"rows": 100, "columns": 8}
print(data.columns())        # ["date", "region", "product", "sales"]
print(data.profile())        # full dataset profile

# Clean in one go
data.clean()

# Chart
data.bar(x="region", y="sales")
data.chart("sales by month")                     # plain English!

# Get automated insights
for note in data.insights():
    print(f"  - {note}")

# Run SQL
print(data.sql("SELECT region, SUM(sales) FROM data GROUP BY region"))

# Generate a report
data.report("report.html")
```

## Supported file formats

| Extension | Format | Load | Export |
|-----------|--------|------|--------|
| `.csv` | Comma-separated values | `tf.load()` | `data.export()` |
| `.xlsx` | Excel workbook | `tf.load()` | `data.export()` |
| `.xls` | Excel 97-2003 | `tf.load()` | — |
| `.json` | JSON | `tf.load()` | `data.export()` |
| `.parquet` | Apache Parquet | `tf.load()` | `data.export()` |

## API overview

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
| `.dtypes` | Column -> dtype mapping (dict) |
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
| `.bar(x, y, save)` | Bar chart |
| `.line(x, y, save)` | Line chart |
| `.scatter(x, y, save)` | Scatter plot |
| `.hist(col, save)` | Histogram |
| `.box(x, y, save)` | Box plot |
| `.heatmap(save)` | Correlation heatmap |
| `.pairplot(save)` | Pairwise scatter matrix |
| `.chart(description)` | Smart chart from plain English |

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

### SQL

| Method | Description |
|--------|-------------|
| `.sql(query)` | Run read-only SQL via DuckDB (table name: `data`) |

### Reports

| Method | Description |
|--------|-------------|
| `.report(path)` | Generate HTML or Excel report |

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

## What Tablofy is not

- **Not a replacement for pandas** — you can always get the underlying DataFrame with `.to_pandas()`
- **Not a big-data tool** — it operates in-memory on a single machine
- **Not a machine-learning library** — no model training or prediction
- **Not a dashboard tool** — reports are static HTML or Excel files
- **Not a database** — SQL runs in-memory against the loaded DataFrame only

## Roadmap

- [x] Load CSV, Excel, JSON, Parquet
- [x] Data exploration (profile, summary, missing, types)
- [x] Data cleaning (duplicates, missing values, column names, dates)
- [x] Transformations (select, drop, sort, filter, group, join)
- [x] Visualization (bar, line, scatter, hist, box, heatmap, pairplot)
- [x] Smart chart from plain-English descriptions
- [x] Rule-based insights
- [x] Statistical helpers (mean, median, outliers, correlation)
- [x] SQL queries via DuckDB
- [x] HTML and Excel reports
- [ ] Interactive charts with Plotly
- [ ] Time-series analysis helpers
- [ ] More chart types (area, pie, violin)
- [ ] Custom theme/style configuration
- [ ] Integration with Jupyter Notebook widgets

## Contributing

Contributions are welcome! Open an issue or pull request on GitHub.

## License

MIT
