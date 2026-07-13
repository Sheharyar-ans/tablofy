# Tablofy API Specification v1.0

**Import convention:** `import tablofy as tf`

---

## 1. Module-Level Functions

### `tf.load(path, **kwargs) -> Table`

Load a file into a `Table`. Convenience wrapper for `Table.load()`.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `path` | `str \| Path` | required | Path to CSV, TSV, .xlsx, or .parquet file |
| `**kwargs` | — | — | Forwarded to the underlying reader (e.g. `sep`, `sheet_name`) |

**Raises:** `FileFormatError` if extension is unsupported.

---

## 2. `Table` Class

### 2.1 Constructor

#### `Table(df, name="")`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `df` | `pd.DataFrame` | required | Data source. Must not be empty. |
| `name` | `str` | `""` | Human-friendly label. Defaults to `"Table"`. |

**Raises:** `EmptyTableError` if `df` is empty.

---

### 2.2 I/O (class methods)

#### `Table.load(path, **kwargs) -> Table`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `path` | `str \| Path` | required | File path |
| `**kwargs` | — | — | Reader options |

**Supported extensions:** `.csv`, `.tsv`, `.xlsx`, `.parquet`  
**Raises:** `FileFormatError`

#### `table.save(path, **kwargs) -> None`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `path` | `str \| Path` | required | Output path |
| `**kwargs` | — | — | Writer options |

**Supported extensions:** `.csv`, `.xlsx`, `.parquet`  
**Raises:** `FileFormatError`

---

### 2.3 Properties

| Property | Returns | Description |
|----------|---------|-------------|
| `table.columns` | `list[str]` | Column names |
| `table.shape` | `tuple[int, int]` | (rows, columns) |
| `table.dtypes` | `dict[str, str]` | Column → dtype string |
| `table._df` | `pd.DataFrame` | Escape hatch — direct pandas access |

---

### 2.4 Preview

#### `table.head(n=5) -> pd.DataFrame`

Return first `n` rows.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `n` | `int` | `5` | Number of rows |

#### `table.schema() -> pd.DataFrame`

Return a DataFrame with columns: `column`, `dtype`, `nulls`.

---

### 2.5 Cleaning

#### `table.clean(drop_duplicates=True, drop_na=False, fill_na=None, strip_whitespace=True) -> Table`

Return a **new** cleaned `Table`. Original is unchanged.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `drop_duplicates` | `bool` | `True` | Remove duplicate rows |
| `drop_na` | `bool` | `False` | Drop rows with any null |
| `fill_na` | `dict \| None` | `None` | Column → value mapping for fill |
| `strip_whitespace` | `bool` | `True` | Strip whitespace on string columns |

---

### 2.6 Profiling

#### `table.profile() -> dict`

Returns a dictionary with:

```python
{
    "name": str,
    "shape": {"rows": int, "columns": int},
    "columns": {
        col_name: {
            "dtype": str,
            "nulls": int,
            "null_pct": float,
            # Numeric columns add:
            "mean": float,
            "std": float,
            "min": float,
            "max": float,
            "median": float,
            # Categorical/object columns add:
            "unique": int,
            "top": str | None,
            "top_freq": int | None,
        }
    },
    "missing_summary": {
        "total_cells": int,
        "total_missing": int,
        "pct_missing": float,
    }
}
```

---

### 2.7 Visualisation

#### `table.chart(kind, x=None, y=None, title=None, interactive=False, **kwargs) -> Figure`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `kind` | `str` | required | See chart types below |
| `x` | `str \| None` | `None` | X-axis column |
| `y` | `str \| None` | `None` | Y-axis column |
| `title` | `str \| None` | `None` | Chart title |
| `interactive` | `bool` | `False` | Use plotly instead of mpl/seaborn |
| `**kwargs` | — | — | Forwarded to the plot function |

**Returns:** `matplotlib.figure.Figure` (default) or `plotly.graph_objects.Figure` (interactive).

**Chart types:**

| `kind` | Required params | Notes |
|--------|----------------|-------|
| `"histogram"` | `x` | Distribution of a numeric column |
| `"scatter"` | `x`, `y` | Two numeric columns |
| `"box"` | `x` (optional) | Box plot of numeric column |
| `"correlation"` | None | Heatmap of numeric correlations |
| `"line"` | `x`, `y` | Line plot |
| `"bar"` | `x`, `y` | Bar plot |

**Raises:** `InvalidChartError` for unknown `kind`.  
**Raises:** `ColumnNotFoundError` if required columns are missing.  
**Raises:** `ValueError` if required params (`x`/`y`) are omitted.

---

### 2.8 SQL Query

#### `table.query(sql) -> Table`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `sql` | `str` | required | SQL. Refer to the table as `self`. |

**Example:** `table.query("SELECT * FROM self WHERE age > 30")`  

**Backend:** DuckDB (in-process, no external DB).  
**Returns:** A new `Table`.

---

### 2.9 Insights

#### `table.insights(max_categories=10) -> list[str]`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `max_categories` | `int` | `10` | Max unique values for categorical detection |

Returns a list of human-readable strings covering:
- Dataset shape
- Missing values summary
- Duplicate rows
- Numeric column ranges (min, max, mean, median)
- Categorical column unique count and mode

---

### 2.10 HTML Report

#### `table.report(path) -> None`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `path` | `str \| Path` | required | Output `.html` path |

Generates a self-contained HTML file with:
- Overview (rows, columns, missing %)
- Column schema table (name, dtype, nulls, null%)
- Insights list
- Tablofy footer

**Backend:** Jinja2.

---

### 2.11 Representation

#### `repr(table) -> str`

Returns `"<Table '{name}' shape=({rows}, {cols})>"`.

---

## 3. Custom Exceptions

| Exception | Inherits | When raised |
|-----------|----------|-------------|
| `TablofyError` | `Exception` | Base for all Tablofy errors |
| `ColumnNotFoundError` | `TablofyError` | Required column(s) missing |
| `FileFormatError` | `TablofyError` | Unsupported or unreadable file |
| `EmptyTableError` | `TablofyError` | DataFrame is empty |
| `InvalidChartError` | `TablofyError` | Unknown chart kind |

---

## 4. Changelog (v1.0)

Initial release.
