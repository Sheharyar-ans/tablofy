# Tablofy Acceptance Tests v1.0

These tests define the complete acceptance criteria for Tablofy v1.0.  
A passing implementation satisfies all scenarios below.

---

## Test Environment

```python
import tablofy as tf
import pandas as pd
import pytest
from pathlib import Path
```

---

## A1. Package Import

| ID | Scenario | Given | When | Then |
|----|----------|-------|------|------|
| A1.1 | Import package | — | `import tablofy as tf` | No error |
| A1.2 | Access `load` | Package imported | `tf.load` | Callable |
| A1.3 | Access `Table` | Package imported | `tf.Table` | Class |
| A1.4 | Access custom errors | Package imported | `tf.TablofyError`, `tf.ColumnNotFoundError`, `tf.FileFormatError`, `tf.EmptyTableError`, `tf.InvalidChartError` | All accessible |

---

## A2. Table Construction

| ID | Scenario | Given | When | Then |
|----|----------|-------|------|------|
| A2.1 | Valid construction | Non-empty DataFrame | `t = tf.Table(df)` | Returns `Table` instance |
| A2.2 | Empty DataFrame rejected | Empty DataFrame | `tf.Table(pd.DataFrame())` | Raises `EmptyTableError` |
| A2.3 | Custom name | DataFrame | `t = tf.Table(df, name="MyData")` | `repr(t)` contains `"MyData"` |
| A2.4 | Default name | DataFrame, no name | `t = tf.Table(df)` | `repr(t)` contains `"Table"` |

---

## A3. Data Loading

| ID | Scenario | Given | When | Then |
|----|----------|-------|------|------|
| A3.1 | Load CSV | Valid CSV file | `t = tf.load("data.csv")` | Returns `Table` with correct shape |
| A3.2 | Load TSV | Valid TSV file | `t = tf.load("data.tsv")` | Returns `Table` with correct shape |
| A3.3 | Load Excel | Valid .xlsx file | `t = tf.load("data.xlsx")` | Returns `Table` with correct shape |
| A3.4 | Load Parquet | Valid .parquet file | `t = tf.load("data.parquet")` | Returns `Table` with correct shape |
| A3.5 | Unsupported format | File `.pdf` | `tf.load("data.pdf")` | Raises `FileFormatError` |
| A3.6 | Module-level load | Valid CSV | `t = tf.load("data.csv")` | Returns same type as `Table.load` |
| A3.7 | Extra kwargs | CSV with custom sep | `tf.load("data.csv", sep="|")` | Correctly parses |

---

## A4. Data Preview

| ID | Scenario | Given | When | Then |
|----|----------|-------|------|------|
| A4.1 | `columns` | Table with cols A, B, C | `t.columns` | `["A", "B", "C"]` |
| A4.2 | `shape` | 10 rows × 3 cols | `t.shape` | `(10, 3)` |
| A4.3 | `dtypes` | Int column "x" | `t.dtypes` | `{"x": "int64"}` |
| A4.4 | `head()` | 10-row table | `t.head(3)` | DataFrame of length 3 |
| A4.5 | `schema()` | Table | `t.schema()` | DataFrame with columns `column`, `dtype`, `nulls` |

---

## A5. Data Cleaning

| ID | Scenario | Given | When | Then |
|----|----------|-------|------|------|
| A5.1 | Original unchanged | Table with data | `t2 = t.clean()` | `t._df` is not mutated |
| A5.2 | Drop duplicates | Table with duplicate rows | `t.clean()` | Duplicate rows removed |
| A5.3 | Fill NA | Column with nulls | `t.clean(fill_na={"x": 0})` | Nulls filled with 0 |
| A5.4 | Drop NA | Rows with nulls | `t.clean(drop_na=True)` | No rows contain null |
| A5.5 | Strip whitespace | Column with padded strings | `t.clean()` | Whitespace stripped |
| A5.6 | Disable whitespace stripping | Column with padded strings | `t.clean(strip_whitespace=False)` | Whitespace preserved |

---

## A6. Profiling

| ID | Scenario | Given | When | Then |
|----|----------|-------|------|------|
| A6.1 | Shape in profile | Table 4×3 | `p = t.profile()` | `p["shape"] == {"rows": 4, "columns": 3}` |
| A6.2 | Missing summary | Table with nulls | `p = t.profile()` | `p["missing_summary"]` keys: `total_cells`, `total_missing`, `pct_missing` |
| A6.3 | Numeric stats | Int column | `p = t.profile()` | Contains `mean`, `std`, `min`, `max`, `median` |
| A6.4 | Categorical stats | Object column | `p = t.profile()` | Contains `unique`, `top`, `top_freq` |
| A6.5 | Column metadata | Any column | `p["columns"][col]` | Contains `dtype`, `nulls`, `null_pct` |

---

## A7. Visualisation

| ID | Scenario | Given | When | Then |
|----|----------|-------|------|------|
| A7.1 | Histogram | Table with numeric col | `fig = t.chart("histogram", x="age")` | Returns `Figure` |
| A7.2 | Scatter | Table with 2 numeric cols | `fig = t.chart("scatter", x="age", y="salary")` | Returns `Figure` |
| A7.3 | Box plot | Table with numeric col | `fig = t.chart("box", x="age")` | Returns `Figure` |
| A7.4 | Line chart | Table with 2 numeric cols | `fig = t.chart("line", x="age", y="salary")` | Returns `Figure` |
| A7.5 | Bar chart | Table with 2 cols | `fig = t.chart("bar", x="name", y="salary")` | Returns `Figure` |
| A7.6 | Correlation heatmap | Table with ≥2 numeric cols | `fig = t.chart("correlation")` | Returns `Figure` |
| A7.7 | Interactive histogram | Table | `fig = t.chart("histogram", x="age", interactive=True)` | Returns plotly `Figure` |
| A7.8 | Invalid chart kind | Table | `t.chart("pie")` | Raises `InvalidChartError` |
| A7.9 | Missing x for scatter | Table | `t.chart("scatter", y="age")` | Raises `ValueError` |
| A7.10 | Missing columns | Table | `t.chart("scatter", x="nonexistent", y="age")` | Raises `ColumnNotFoundError` |

---

## A8. SQL Query

| ID | Scenario | Given | When | Then |
|----|----------|-------|------|------|
| A8.1 | Basic SELECT | Table with data | `r = t.query("SELECT * FROM self")` | Returns `Table` with same shape |
| A8.2 | WHERE filter | Table | `r = t.query("SELECT * FROM self WHERE age > 30")` | Returns filtered Table |
| A8.3 | Column selection | Table | `r = t.query("SELECT name FROM self")` | Returns Table with one column |
| A8.4 | Aggregation | Table | `r = t.query("SELECT AVG(age) AS avg_age FROM self")` | Returns Table with aggregated result |
| A8.5 | Original unchanged | Table | `r = t.query("...")` | `t._df` is not mutated |

---

## A9. Insights

| ID | Scenario | Given | When | Then |
|----|----------|-------|------|------|
| A9.1 | Returns list | Table | `obs = t.insights()` | Returns `list[str]` |
| A9.2 | Non-empty | Non-empty Table | `obs = t.insights()` | `len(obs) > 0` |
| A9.3 | Contains shape | Table named "Sales" | `obs = t.insights()` | At least one observation mentions "Sales" |
| A9.4 | Handles empty columns gracefully | Table with all-null column | `obs = t.insights()` | No crash; skips column |
| A9.5 | Categorical detection | Column with ≤10 unique | `obs = t.insights()` | Mentions mode |

---

## A10. HTML Report

| ID | Scenario | Given | When | Then |
|----|----------|-------|------|------|
| A10.1 | File created | Table | `t.report("out.html")` | `Path("out.html").exists()` |
| A10.2 | Contains title | Table named "Sales" | Content of `out.html` | Contains "Report: Sales" |
| A10.3 | Contains overview | Table | Content of `out.html` | Contains "Rows", "Columns", "Missing cells" |
| A10.4 | Contains column table | Table | Content of `out.html` | Contains `<th>Column</th>` |
| A10.5 | Contains insights | Table | Content of `out.html` | Contains `<li>` elements |
| A10.6 | Self-contained | Table, `report()` | `out.html` | No external CSS/JS dependencies needed |

---

## A11. File Export

| ID | Scenario | Given | When | Then |
|----|----------|-------|------|------|
| A11.1 | Save CSV | Table | `t.save("out.csv")` | `Path("out.csv").exists()` |
| A11.2 | Save Excel | Table | `t.save("out.xlsx")` | `Path("out.xlsx").exists()` |
| A11.3 | Save Parquet | Table | `t.save("out.parquet")` | `Path("out.parquet").exists()` |
| A11.4 | Save unsupported | Table | `t.save("out.json")` | Raises `FileFormatError` |

---

## A12. Column Validation

| ID | Scenario | Given | When | Then |
|----|----------|-------|------|------|
| A12.1 | Valid columns pass | Table with col "x" | `t._require_columns(["x"])` | No error |
| A12.2 | Invalid column fails | Table without col "z" | `t._require_columns(["z"])` | Raises `ColumnNotFoundError` |
| A12.3 | Error message | Missing cols | Catch error | `str(e)` contains missing column name(s) |

---

## A13. Edge Cases

| ID | Scenario | Given | When | Then |
|----|----------|-------|------|------|
| A13.1 | Single row | DataFrame with 1 row | `Table(df_single)` | Works, `shape == (1, N)` |
| A13.2 | Single column | DataFrame with 1 col | `Table(df_one_col)` | Works, `shape == (N, 1)` |
| A13.3 | All null column | Column entirely NaN | `t.chart("histogram", x="null_col")` | Draws empty chart (no crash) |
| A13.4 | No numeric columns | All string columns | `t.chart("correlation")` | Raises `ValueError` |
| A13.5 | Boolean column | Column of bools | `t.profile()` | Treated as categorical |
| A13.6 | Very long column names | Column named "a"*100 | `t.profile()` | Works; names preserved |
| A13.7 | Unicode column names | Column named "姓名" | `t.profile()` | Works |
| A13.8 | Zero-row after clean | All rows filtered | `t.clean(drop_na=True)` on all-null | Returns Table with 0 rows (no crash) |

---

## A14. Regression

| ID | Scenario | Given | When | Then |
|----|----------|-------|------|------|
| A14.1 | Chained API | Table | `t.clean().profile()` | Returns dict (profile result) |
| A14.2 | Chained clean → chart | Table | `t.clean().chart("histogram", x="age")` | Returns Figure |
| A14.3 | Immutable operations | Table | Multiple clean/profile/chart calls | `t._df` never mutated |
| A14.4 | `repr` after operations | Table | After chain | `repr(t)` unchanged |

---

## A15. Lint & Quality

| ID | Scenario | Given | When | Then |
|----|----------|-------|------|------|
| A15.1 | ruff zero errors | Source code | `ruff check src/ tests/` | Exit code 0 |
| A15.2 | Public method docstrings | Every public method | Inspect `__doc__` | All non-empty |
| A15.3 | No eval in source | All `.py` files | `grep -r "eval(" src/` | No matches (except in comments/strings) |
