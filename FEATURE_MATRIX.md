# Tablofy Feature Matrix v1.0

**Legend:** ✅ v1.0 | 🚫 Excluded | 🔄 Postponed (potential v2)

---

## 1. Data Loading

| Feature | Status | Notes |
|---------|--------|-------|
| Load CSV | ✅ | Via `pd.read_csv` |
| Load TSV | ✅ | Via `pd.read_csv(sep="\t")` |
| Load Excel (.xlsx) | ✅ | Via `pd.read_excel` |
| Load Parquet | ✅ | Via `pd.read_parquet` |
| Load JSON | 🚫 | Postponed; not in v1 scope |
| Load from URL | 🚫 | v1 is local filesystem only |
| Load from clipboard | 🚫 | Postponed |
| Load from database | 🚫 | Not a database app |
| Cloud storage (S3, GCS) | 🚫 | Out of scope |

---

## 2. Data Preview

| Feature | Status | Notes |
|---------|--------|-------|
| `table.columns` | ✅ | List of column names |
| `table.shape` | ✅ | (rows, cols) tuple |
| `table.dtypes` | ✅ | Column → dtype dict |
| `table.head(n)` | ✅ | First n rows |
| `table.schema()` | ✅ | Dtype + null count per column |
| `table.tail(n)` | 🚫 | Not in v1; use escape hatch |
| `table.describe()` | 🚫 | Not in v1; use `profile()` |
| `table.info()` | 🚫 | Not in v1; use `schema()` |
| Row sampling | 🚫 | Postponed |

---

## 3. Data Cleaning

| Feature | Status | Notes |
|---------|--------|-------|
| Drop duplicates | ✅ | `clean(drop_duplicates=True)` |
| Drop rows with nulls | ✅ | `clean(drop_na=True)` |
| Fill nulls (column-specific) | ✅ | `clean(fill_na={"col": val})` |
| Strip whitespace | ✅ | `clean(strip_whitespace=True)` |
| Column rename | 🔄 | Pending — use `query("SELECT ... AS ...")` |
| Type casting | 🔄 | Pending — use escape hatch |
| Outlier removal | 🚫 | Deferred to v2 |
| String normalisation | 🚫 | Deferred to v2 |
| Date parsing | 🚫 | Deferred to v2 |

---

## 4. Profiling / Statistics

| Feature | Status | Notes |
|---------|--------|-------|
| Row & column count | ✅ | Part of `profile()` |
| Missing value summary | ✅ | Total, nulls per column, percents |
| Numeric: mean, std, min, max, median | ✅ | Per numeric column |
| Categorical: unique count, mode, freq | ✅ | Per object/category column |
| Correlation matrix | ✅ | Via `chart("correlation")` |
| Histogram | ✅ | Via `chart("histogram")` |
| Hypothesis tests (t-test, chi2) | 🚫 | Deferred to v2 |
| Distribution fitting | 🚫 | Deferred to v2 |
| Skewness / kurtosis | 🚫 | Deferred to v2 |
| Quantiles / percentiles | 🚫 | Deferred to v2 |

---

## 5. Visualisation

| Feature | Status | Notes |
|---------|--------|-------|
| Histogram | ✅ | Seaborn + matplotlib |
| Scatter plot | ✅ | Seaborn + matplotlib |
| Box plot | ✅ | Seaborn + matplotlib |
| Line chart | ✅ | Seaborn + matplotlib |
| Bar chart | ✅ | Seaborn + matplotlib |
| Correlation heatmap | ✅ | Matplotlib heatmap |
| All charts interactive | ✅ | Via `interactive=True` (plotly) |
| Custom colours | ✅ | Via `**kwargs` passed to plot function |
| Figure size | ✅ | Via `**kwargs` / `figsize` |
| Pie chart | 🚫 | Not statistical; use escape hatch |
| Violin plot | 🚫 | Deferred to v2 |
| Pair plot | 🚫 | Deferred to v2 |
| Facet grids | 🚫 | Deferred to v2 |
| 3D plots | 🚫 | Out of scope |
| Custom chart registration | 🚫 | Use escape hatch |

---

## 6. SQL Query

| Feature | Status | Notes |
|---------|--------|-------|
| `SELECT` queries | ✅ | Via DuckDB |
| `WHERE` filtering | ✅ | Standard SQL |
| `GROUP BY` / aggregation | ✅ | Standard SQL |
| `JOIN` across tables | ✅ | Register multiple tables manually |
| `ORDER BY` | ✅ | Standard SQL |
| `LIMIT` | ✅ | Standard SQL |
| Window functions | ✅ | DuckDB supports them |
| Write queries (INSERT, UPDATE, DELETE) | 🚫 | Tablofy is read-only analytics |
| CREATE TABLE / schema management | 🚫 | Not a database app |
| Persistent DuckDB database | 🚫 | In-memory only per `query()` call |

---

## 7. Insights

| Feature | Status | Notes |
|---------|--------|-------|
| Shape observation | ✅ | "N rows × M columns" |
| Missing data observation | ✅ | Total + percent |
| Duplicate observation | ✅ | Count of duplicates |
| Numeric column summary | ✅ | Range, mean, median |
| Categorical column summary | ✅ | Unique count, mode |
| Trend detection | 🚫 | Deferred to v2 |
| Anomaly detection | 🚫 | Deferred to v2 |
| Correlation commentary | 🚫 | Deferred to v2 |

---

## 8. HTML Report

| Feature | Status | Notes |
|---------|--------|-------|
| Overview section | ✅ | Rows, columns, missing % |
| Column schema table | ✅ | Name, dtype, nulls |
| Insights list | ✅ | Rendered from `insights()` |
| Custom branding | 🚫 | Static template; use escape hatch |
| Embedded charts | 🚫 | Deferred to v2 |
| Interactive tables | 🚫 | Deferred to v2 |
| Export as PDF | 🚫 | Browser Print → PDF is a workaround |

---

## 9. File Export

| Feature | Status | Notes |
|---------|--------|-------|
| Save CSV | ✅ | `save("file.csv")` |
| Save Excel | ✅ | `save("file.xlsx")` |
| Save Parquet | ✅ | `save("file.parquet")` |
| Save JSON | 🚫 | Not in v1 |
| Save HTML | ✅ | Via `report()` (not raw data export) |
| Save clipboard | 🚫 | Postponed |

---

## 10. Escape Hatch

| Feature | Status | Notes |
|---------|--------|-------|
| Access raw DataFrame | ✅ | `table._df` (convention: private, use at own risk) |
| Use any pandas method | ✅ | Everything accessible via `_df` |

---

## 11. Cross-Cutting

| Feature | Status | Notes |
|---------|--------|-------|
| Custom exceptions | ✅ | `TablofyError` hierarchy |
| Input validation | ✅ | Column checks, empty checks, format checks |
| Docstrings on all public methods | ✅ | Required by spec |
| pytest coverage | ✅ | Required by spec |
| ruff lint (zero errors) | ✅ | Required by spec |
| Logging | 🚫 | v1 uses exceptions only; logging deferred |
| Progress bars | 🚫 | Not needed at v1 scale |
| Parallel execution | 🚫 | Out of scope |
| Caching | 🚫 | Out of scope |
