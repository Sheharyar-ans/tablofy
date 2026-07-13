# Tablofy — Product Requirements Document

**Version:** 1.0  
**Status:** Draft  
**Last updated:** 2026-07-13

---

## 1. Product Vision

Tablofy is a beginner-friendly Python data analytics library that wraps pandas, NumPy, Matplotlib, Seaborn, Plotly, DuckDB, PyArrow, OpenPyXL, and Jinja2 behind a single, simple API. Users should be able to complete a full analytics workflow — load, clean, explore, visualise, query, and report — without learning the intricacies of each backend library.

## 2. Target Audience

- Data analysts who know Python basics but not pandas internals
- Students learning data analytics
- Professionals who need quick ad-hoc analysis without boilerplate
- Teams wanting a consistent, minimal API for routine analytics tasks

## 3. Design Principles

1. **Simplicity first.** One import (`import tablofy as tf`), one entry point (`tf.load()` → `Table`), all operations are method calls on `Table`.
2. **Backend engines, not clones.** Do not reimplement pandas, NumPy, Matplotlib, Seaborn, Plotly, DuckDB, PyArrow, or OpenPyXL. Use them as dependencies and expose a curated subset of their power.
3. **No magic strings, no eval.** All operations are explicit method calls. No `eval()`, no dynamic code generation.
4. **Fail early, fail clearly.** Every public method validates inputs. Errors use custom exception types with human-readable messages.
5. **Batteries included.** The library ships with sensible defaults but allows override via keyword arguments.
6. **Escape hatch.** Users who outgrow the API can access the underlying pandas DataFrame via `table._df`.

## 4. What Tablofy v1 Builds

| Area | Description |
|------|-------------|
| Data loading | Load CSV, TSV, Excel (.xlsx), Parquet files |
| Data preview | `head()`, `columns`, `shape`, `dtypes`, `schema()` |
| Data cleaning | Drop duplicates, fill/drop missing values, strip whitespace |
| Data exploration | `profile()` returning summary stats for every column |
| Data transformation | Sort, filter, rename columns via DuckDB SQL |
| Visualisation | Histogram, scatter, box, line, bar, correlation heatmap (matplotlib/seaborn or plotly) |
| Analytics insights | Auto-generated text observations (shape, missing data, duplicates, ranges, modes) |
| Basic statistics | Mean, median, std, min, max, null counts per column |
| SQL query | Run SQL directly against the table via DuckDB |
| HTML report | Self-contained HTML page with overview, column schema, and insights |
| Excel export | Save table to .xlsx |
| Interactive charts | Plotly-powered charts with `interactive=True` |
| Escape hatch | Direct access to `table._df` (pandas DataFrame) |

## 5. What Tablofy v1 Does NOT Build

| Area | Exclusion rationale |
|------|-------------------|
| Machine learning / scikit-learn | Out of scope for v1. Tablofy is analytics-only. |
| Deep learning / PyTorch / TensorFlow | Out of scope. |
| AI chatbot / ChatGPT / LLM integration | Not an analytics feature. |
| SaaS / web dashboard | Tablofy is a Python library, not a service. |
| API server / REST endpoints | Not an analytics feature. |
| Database app / ORM | DuckDB is used for in-process SQL only. |
| Login / authentication system | Not applicable. |
| Real-time streaming | Out of scope. |
| Custom chart types beyond the curated list | v1 offers 6 chart types. Custom charts should use the escape hatch. |
| Dashboard builder | Use the escape hatch + Plotly Dash if needed. |
| Data pipelines / ETL framework | Minimal transform only. Not an ETL tool. |
| Cloud storage connectors | Only local file system in v1. |
| Statistical hypothesis testing | Deferred to v2. |
| Time-series decomposition | Deferred to v2. |

## 6. Constraints

- Python >= 3.10
- Windows, macOS, Linux compatible
- No external service calls
- No telemetry or data collection
- No `eval()` or `exec()`
- All public methods must have docstrings
- Every public method must have at least one pytest test

## 7. Success Metrics (v1)

- User can go from `pip install tablofy` to a full HTML report in under 5 minutes
- 100% of public methods have passing tests
- Zero lint errors (ruff, default ruleset)
- All user-facing errors use custom exception types (not raw `ValueError` from backends)

## 8. User Flow (Canonical Example)

```python
import tablofy as tf

# 1. Load
data = tf.load("sales.csv")

# 2. Preview
print(data.shape, data.columns)

# 3. Clean
data = data.clean()

# 4. Profile
stats = data.profile()

# 5. Visualise
data.chart("histogram", x="revenue")
data.chart("scatter", x="revenue", y="cost", interactive=True)

# 6. SQL query
high_value = data.query("SELECT * FROM self WHERE revenue > 10000")

# 7. Insights
for note in data.insights():
    print(note)

# 8. Report
data.report("report.html")
```
