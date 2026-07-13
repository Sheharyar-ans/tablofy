# Tablofy Architecture v1.0

---

## 1. Overview

Tablofy follows a **facade pattern**. A single `Table` class exposes a simplified API that delegates to specialised sub-modules. Each sub-module imports and uses one or more backend libraries directly; Tablofy never reimplements backend logic.

```
┌──────────────────────────────────────────────────┐
│                   user code                       │
│  import tablofy as tf                             │
│  data = tf.load("file.csv")                       │
│  data.clean().profile()                           │
└────────────────────┬─────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────┐
│               tablofy (public API)                 │
│  ┌──────────────────────────────────────────────┐ │
│  │  __init__.py                                 │ │
│  │  • load() → Table                            │ │
│  │  • Table class                               │ │
│  │  • Custom exception exports                  │ │
│  └──────┬──────────────────┬───────────────────┘ │
└─────────┼──────────────────┼──────────────────────┘
          │ delegates        │ delegates
┌─────────▼──────────┐ ┌─────▼──────────────────────┐
│  public methods     │ │  sub-module functions      │
│  on Table           │ │                            │
│                     │ │  _clean() → new Table      │
│  .clean() ──────────┼─►  _profile() → dict         │
│  .profile() ────────┼─►  _chart() → Figure         │
│  .chart() ──────────┼─►  _insights() → list[str]   │
│  .insights() ───────┼─►  _report() → writes HTML   │
│  .report() ─────────┼─►                            │
│  .query() ──────────┼─►  duckdb directly           │
└─────────────────────┘  └───────────────────────────┘
```

---

## 2. Module Layout

```
src/tablofy/
├── __init__.py       # Public API: load(), Table, exceptions
├── table.py          # Core Table class
├── errors.py         # Custom exception hierarchy
├── _clean.py         # clean() implementation
├── _profile.py       # profile() implementation
├── _chart.py         # chart() implementation (mpl/seaborn/plotly)
├── _insights.py      # insights() implementation
├── _report.py        # report() implementation (Jinja2)
```

**Naming convention:** Public modules are un-prefixed. Private sub-modules (implementation details) are prefixed with `_`. Users should not import from `_` modules directly.

---

## 3. Data Flow

### 3.1 Loading

```
tf.load("file.csv")
  └── Table.load("file.csv")
        └── pd.read_csv("file.csv")       # or read_excel / read_parquet
              └── Table(df, name="file")   # wraps in Table
```

### 3.2 Cleaning

```
table.clean(fill_na={"age": 0})
  └── _clean(table, fill_na={"age": 0})
        └── df = table._df.copy()
        └── Apply transformations on df
        └── return Table(df, name=table.name)
```

### 3.3 Charting

```
table.chart("scatter", x="age", y="salary")
  └── _chart(table, "scatter", x="age", y="salary")
        ├── interactive=False → seaborn/matplotlib
        │     └── sns.scatterplot(data=df, x="age", y="salary")
        │     └── return fig (matplotlib.figure.Figure)
        │
        └── interactive=True → plotly
              └── px.scatter(df, x="age", y="salary")
              └── return fig (plotly.graph_objects.Figure)
```

### 3.4 SQL Query

```
table.query("SELECT * FROM self WHERE age > 30")
  └── conn = duckdb.connect()
  └── conn.register("self", self._df)
  └── result = conn.execute(sql).df()
  └── conn.close()
  └── return Table(result)
```

### 3.5 HTML Report

```
table.report("report.html")
  └── _report(table, "report.html")
        ├── _profile(table)                    # gather stats
        ├── _insights(table)                   # gather observations
        └── Template(HTML).render(...)          # Jinja2 render
        └── Path("report.html").write_text(html)
```

---

## 4. Error Handling Strategy

| Layer | Strategy |
|-------|----------|
| Table constructor | Raise `EmptyTableError` if DataFrame is empty |
| I/O methods | Catch backend errors, wrap in `FileFormatError` |
| Column validation | `_require_columns()` raises `ColumnNotFoundError` |
| Chart dispatch | Raise `InvalidChartError` for unknown chart kind |
| SQL | DuckDB exceptions propagate as-is (query errors are user SQL issues) |
| All other backends | Exceptions propagate with original message |

Custom exceptions all inherit from `TablofyError` so callers can catch broadly:

```python
from tablofy import TablofyError
try:
    data = tf.load("bad.csv")
except TablofyError as e:
    print(f"Tablofy error: {e}")
```

---

## 5. Backend Dependencies

| Backend | Used in | Purpose |
|---------|---------|---------|
| `pandas` | `table.py`, `_clean.py`, `_profile.py`, `_chart.py`, `_insights.py` | DataFrame operations |
| `numpy` | `_profile.py` (indirect via pandas) | Numerical operations |
| `matplotlib` | `_chart.py` | Figure creation |
| `seaborn` | `_chart.py` | Statistical charts |
| `plotly` | `_chart.py` | Interactive charts |
| `duckdb` | `table.py` | SQL queries |
| `pyarrow` | `table.py` (via pandas) | Parquet support |
| `openpyxl` | `table.py` (via pandas) | Excel read/write |
| `jinja2` | `_report.py` | HTML report templates |

---

## 6. Design Decisions

### 6.1 Why a facade pattern?

New users should not need to learn five different library APIs. A single `Table` object with `load()`, `clean()`, `profile()`, `chart()`, `insights()`, `report()` covers 90 % of routine analytics tasks.

### 6.2 Why sub-modules instead of a single file?

Each sub-module has one responsibility. This keeps `table.py` under 200 lines, makes testing isolated, and allows contributors to work on `_chart.py` without touching `_clean.py`.

### 6.3 Why `interactive=True` instead of a separate method?

Keeps the API surface small. One `chart()` method, one more keyword argument.

### 6.4 Why expose `_df` as an escape hatch?

Users who outgrow the facade should not be trapped. Direct pandas access is an explicit opt-in (the underscore signals "internal, use at your own risk").

### 6.5 Why not use `eval()`?

Security and maintainability. All operations are explicit method calls or parsed SQL (DuckDB handles its own parsing).

---

## 7. Testing Strategy

- **Unit tests:** Every public method on `Table` has at least one test.
- **File I/O tests:** Use `tmp_path` fixtures to avoid polluting the repo.
- **Chart tests:** Verify the figure object is returned (not None), not pixel output.
- **Lint:** `ruff check src/ tests/` must pass with zero errors.

---

## 8. Build & Distribution

- **Build system:** `setuptools` via `pyproject.toml`
- **Package layout:** `src/` layout (recommended by PEP 517/518)
- **Python requirement:** `>= 3.10`
- **Distribution:** PyPI (planned)
