# Tablofy

**One import to rule them all.**  
*Zero-boilerplate data loading, cleaning, visualization, ML, and reporting — all from a single import.*

[![PyPI](https://img.shields.io/pypi/v/tablofy)](https://pypi.org/project/tablofy/)
[![Python](https://img.shields.io/pypi/pyversions/tablofy)](https://pypi.org/project/tablofy/)
[![License](https://img.shields.io/pypi/l/tablofy)](LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/tablofy)](https://pypi.org/project/tablofy/)

---

## Why Tablofy?

Stop writing the same 10 imports at the top of every notebook. Tablofy wraps **pandas, matplotlib, seaborn, Plotly, scikit-learn, statsmodels, DuckDB, and more** behind a single, consistent API.

| Task | Raw Python | Tablofy |
|---|---|---|
| Import | `import pandas as pd`<br>`import numpy as np`<br>`import matplotlib.pyplot as plt`<br>`import seaborn as sns`<br>... | `import tablofy as tf` |
| Load CSV | `pd.read_csv("data.csv")` | `tf.load("data.csv")` |
| Clean | 5–10 lines of boilerplate | `df.clean()` |
| Chart | `plt.figure(); sns.barplot(...); plt.show()` | `df.bar(x="a", y="b")` |
| ML pipeline | 20+ lines (split, scale, train, eval) | `model = df.ml.predict(target, features, method="regression")` |
| Report | Manual HTML/CSS/Jinja wiring | `df.report("report.html")` |

```python
import tablofy as tf          # ← the only import you'll ever need
```

---

## Table of Contents

- [Quickstart](#quickstart)
- [Installation](#installation)
- [Unified Engine Shortcuts](#unified-engine-shortcuts)
- [Bulletproof Data Loading](#bulletproof-data-loading)
- [Smart Column Selection & Wrangling](#smart-column-selection--wrangling)
- [Cleaning Pipeline](#cleaning-pipeline)
- [Static & Interactive Visualizations](#static--interactive-visualizations)
- [Applied ML Engine](#applied-ml-engine)
- [Time-Series Engine](#time-series-engine)
- [SQL on DataFrames](#sql-on-dataframes)
- [Theming](#theming)
- [HTML Report Compiler](#html-report-compiler)
- [Jupyter Widget Explorer](#jupyter-widget-explorer)
- [Supported File Formats](#supported-file-formats)
- [API Overview](#api-overview)
- [Contributing](#contributing)
- [License](#license)

---

## Quickstart

A complete end-to-end workflow with the Titanic dataset — every line in a single script:

```python
import tablofy as tf

# 1. Load directly from a URL (bypasses local file checks automatically)
df = tf.load("https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv")

# 2. Clean: drop duplicates, fill missing, snake_case columns, parse dates
df.clean()

# 3. Explore with bracket selection
print(df['Survived'].value_counts())          # 0    549, 1    342
first_class = df[['Pclass', 'Fare', 'Age']]   # returns a new TablofyFrame
print(first_class.preview())

# 4. Visualise
df.violin(x="Sex", y="Age")
tf.show()                                      # displays all figures

# 5. Train a classifier and print metrics
model = df.ml.predict(
    target="Survived",
    features=["Pclass", "Age", "Fare", "SibSp", "Parch"],
    method="classification",
)
print(f"Model trained: {type(model).__name__}")

# 6. Export a shareable HTML report
df.report("titanic_report.html")
```

> **That's it.** No `import pandas as pd`. No `import matplotlib.pyplot as plt`. No `train_test_split`, `StandardScaler`, or metric imports. Tablofy handles it all.

---

## Installation

```bash
pip install tablofy
```

Requires Python 3.9 or later.

### Optional feature extras

Keep the core lean; opt in to heavier libraries as needed:

| Command | What you get |
|---|---|
| `pip install "tablofy[all]"` | Everything below |
| `pip install "tablofy[viz]"` | Interactive Plotly charts (`interactive=True`) |
| `pip install "tablofy[ml]"` | Scikit-learn ML pipeline (`df.ml.predict`) |
| `pip install "tablofy[stats]"` | SciPy / Statsmodels advanced statistics |
| `pip install "tablofy[widgets]"` | Jupyter Notebook widget explorer |
| `pip install "tablofy[scraping]"` | Web scraping with BeautifulSoup & Requests |
| `pip install "tablofy[fast]"` | Polars / PyArrow for large datasets |
| `pip install "tablofy[dl]"` | PyTorch / TensorFlow deep learning |

### TestPyPI

```bash
pip install -i https://test.pypi.org/simple/ tablofy
```

---

## Unified Engine Shortcuts

Tablofy exposes **pandas** and **numpy** directly on the `tf` namespace so you never need to import them separately.

```python
import tablofy as tf

# pandas and numpy — always available
print(tf.pd.DataFrame({"x": [1, 2, 3]}))      # no import needed
print(tf.np.array([1, 2, 3]))                  # no import needed

# Display all matplotlib/seaborn figures
tf.show()                                       # calls plt.show() internally
```

> `tf.show()` dynamically imports `matplotlib.pyplot` only when called — no overhead at import time.

---

## Bulletproof Data Loading

`tf.load()` auto-detects the file format from the extension and **transparently handles both local files and web URLs**.

- **Local files**: validated for existence (raises `TablofyFileError` if missing).
- **Web URLs** (`http://` or `https://`): local file checks are bypassed automatically.

```python
# Local file — extension is auto-detected
df = tf.load("data.csv")

# Web URL — no manual download needed
df = tf.load("https://example.com/dataset.csv")

# Also supports Excel, JSON, and Parquet
df = tf.load("data.parquet")

# Explicit web loader (alias)
df = tf.load_web("https://example.com/data.csv")
```

**Supported formats:** `.csv`, `.xlsx`, `.xls`, `.json`, `.parquet`.

---

## Smart Column Selection & Wrangling

`TablofyFrame` supports **native square-bracket subscripting** just like a pandas DataFrame, plus all the familiar transformation methods.

```python
# Bracket selection — returns a pandas Series
ages = df['Age']
print(ages.unique())                # chaining works naturally

# Bracket selection with a list — returns a new TablofyFrame
subset = df[['Pclass', 'Fare', 'Age']]
print(type(subset))                 # <class 'TablofyFrame'>

# Smart selection with case-insensitive fallback
df.select("pclass", "fare")         # matches even if casing differs

# Transform & chain
df.select("Age", "Fare") \
  .drop("Fare") \
  .rename({"Age": "years"}) \
  .sort("years", descending=True) \
  .preview(3)
```

| Method | Returns | Description |
|---|---|---|
| `df['col']` | `pd.Series` | Single column by name |
| `df[['a','b']]` | `TablofyFrame` | Subset of columns |
| `.select(*cols)` | `TablofyFrame` | Case-insensitive column selector |
| `.drop(col)` | `TablofyFrame` | Remove one column |
| `.rename(mapping)` | `TablofyFrame` | Rename columns |
| `.filter(expr)` | `TablofyFrame` | Query by pandas expression |
| `.sort(by, descending)` | `TablofyFrame` | Sort by column |
| `.group(by)` | `GroupedFrame` | Group for aggregation |
| `.pivot(index, columns, values)` | `TablofyFrame` | Pivot table |
| `.join(other, on, how)` | `TablofyFrame` | Merge on shared key |

---

## Cleaning Pipeline

```python
# One-shot cleaning — duplicates, missing values, column names, dates, whitespace
df.clean()

# View what was done
report = df.clean_report()
print(report['summary_text'])
```

| Argument | Default | Effect |
|---|---|---|
| `duplicates` | `True` | Remove duplicate rows |
| `missing` | `"smart"` | Fill numeric with median, text with mode |
| `columns` | `"snake_case"` | Normalise column names |
| `dates` | `True` | Parse date-like object columns |
| `text` | `True` | Strip whitespace, drop fully-null columns |

---

## Static & Interactive Visualizations

Every chart method accepts **`interactive=True`** to switch from matplotlib/seaborn to Plotly.

```python
# Static (matplotlib / seaborn)
df.bar(x="Pclass", y="Fare")

# Interactive (requires: pip install tablofy[viz])
df.bar(x="Pclass", y="Fare", interactive=True)

# All chart types
df.line(x="Age", y="Fare")
df.scatter(x="Age", y="Fare")
df.hist(column="Age")
df.box(x="Sex", y="Age")
df.violin(x="Sex", y="Age")
df.pie(labels="Pclass", values="Fare")
df.area(x="Age", y="Fare")
df.heatmap()
df.pairplot()

# Smart chart from plain English
df.chart("survival by passenger class")
```

| Argument | Type | Description |
|---|---|---|
| `interactive` | `bool` | Set to `True` for a Plotly figure (requires `tablofy[viz]`) |
| `save` | `str or None` | File path to save (`.png` for static, `.html` for interactive) |

> **Pro tip:** Use `tf.show()` after creating multiple static charts to display them all at once.

---

## Applied ML Engine

No manual imports. No boilerplate. Just pick your target, features, and method.

```python
# Requires: pip install tablofy[ml]

# Classification (RandomForestClassifier)
model = df.ml.predict(
    target="Survived",
    features=["Pclass", "Age", "Fare", "SibSp", "Parch"],
    method="classification",
)

# Regression (LinearRegression)
model = df.ml.predict(
    target="Fare",
    features=["Pclass", "Age", "SibSp", "Parch"],
    method="regression",
)
```

**What happens under the hood:**
1. Numerical NaNs are filled with column means
2. Data is split into train/test sets (`test_size=0.2`)
3. Features are scaled with `StandardScaler`
4. The model is trained (RandomForestClassifier or LinearRegression)
5. Evaluation metrics are printed to the terminal
6. The trained estimator is returned

**Classification output:**
```
==================================================
Model type: classification
Target column: Survived
Features (5): ['Pclass', 'Age', 'Fare', 'SibSp', 'Parch']
Train size: 712  |  Test size: 179
--------------------------------------------------
Accuracy: 0.8212
              precision    recall  f1-score   support
           0       0.83      0.87      0.85       110
           1       0.78      0.72      0.75        69
    accuracy                           0.82       179
==================================================
```

**Regression output:**
```
==================================================
Model type: regression
Target column: Fare
Features (4): ['Pclass', 'Age', 'SibSp', 'Parch']
Train size: 712  |  Test size: 179
--------------------------------------------------
Mean Squared Error: 1258.4321
R² Score: 0.4231
==================================================
```

| Parameter | Default | Description |
|---|---|---|
| `target` | (required) | Name of the column to predict |
| `features` | (required) | List of feature column names |
| `method` | `"classification"` | `"classification"` or `"regression"` |
| `test_size` | `0.2` | Fraction of data for testing |
| `random_state` | `42` | Random seed for reproducibility |

---

## Time-Series Engine

```python
# Convert a date column to datetime and promote it to the index
df.ts.set_time_index("date")

# Resample to weekly averages
weekly = df.ts.resample(rule="W", agg="mean")

# Rolling mean — returns a new TablofyFrame
rolling = df.ts.rolling(window=7, col="sales")
print(type(rolling))  # <class 'TablofyFrame'>

# Detect trend direction
trend = df.ts.detect_trend("sales")
# → {"direction": "upward", "slope": 40.0, "strength": "strong"}
```

| Method | Returns | Description |
|---|---|---|
| `.ts.set_time_index(col)` | `TablofyFrame` (self) | Parse & promote column to DatetimeIndex |
| `.ts.resample(rule, agg)` | `TablofyFrame` | Resample by offset alias |
| `.ts.rolling(window, col)` | `TablofyFrame` | Rolling mean as a new frame |
| `.ts.detect_trend(col)` | `dict` | Direction, slope, and strength |

---

## SQL on DataFrames

Run read-only SQL queries against any `TablofyFrame` using DuckDB — the table is automatically registered as `data`.

```python
result = df.sql("""
    SELECT Pclass, ROUND(AVG(Fare), 2) AS avg_fare
    FROM data
    WHERE Age > 30
    GROUP BY Pclass
    ORDER BY avg_fare DESC
""")
```

---

## Theming

Apply a consistent visual style to **all charts** (both static and interactive) in one call.

```python
tf.set_theme("dark")       # dark mode with neon accents
tf.set_theme("modern")     # clean, minimal, sans-serif
tf.set_theme("pastel")     # soft, bright colours
tf.set_theme("classic")    # academic, serif, no grid
tf.set_theme("default")    # reset to defaults

# Custom palette
tf.set_theme("modern", palette=["#ff6b6b", "#4ecdc4"])
```

Themes propagate to matplotlib rcParams, seaborn palettes, and Plotly templates simultaneously.

---

## HTML Report Compiler

Bundle your entire analysis into a single, self-contained, shareable HTML file.

```python
# Minimal report
df.report("analysis.html")

# With embedded chart images
df.report("analysis.html", charts=[
    ("Survival by Class", "charts/class_survival.png"),
    ("Age Distribution",  "charts/age_dist.png"),
])
```

Also supports Excel reports via `.report("analysis.xlsx")`.

---

## Jupyter Widget Explorer

Inside a Jupyter notebook, launch a fully interactive dashboard with zero UI code:

```python
df.explore_interactive()
```

Renders: column picker, dynamic filters (sliders + multi-select), live table preview, and an auto-updating chart.

Requires: `pip install tablofy[widgets]`

---

## Supported File Formats

| Extension | Format | Load | Export |
|---|---|---|---|
| `.csv` | Comma-separated values | `tf.load()` | `data.export()` |
| `.xlsx` | Excel workbook | `tf.load()` | `data.export()` |
| `.xls` | Excel 97–2003 | `tf.load()` | — |
| `.json` | JSON | `tf.load()` | `data.export()` |
| `.parquet` | Apache Parquet | `tf.load()` | `data.export()` |

---

## API Overview

### Loading

| Method | Description |
|---|---|
| `tf.load(path)` | Load any supported file (auto-detects format) |
| `tf.load_web(url)` | Load a CSV or JSON directly from a URL |
| `TablofyFrame(df, name)` | Wrap an existing pandas DataFrame |

### Exploration

| Method | Description |
|---|---|
| `.preview(n=5)` | First `n` rows |
| `.head(n=5)` | Alias for `.preview()` |
| `.shape()` | `{"rows": N, "columns": M}` |
| `.columns()` | List of column names |
| `.dtypes` | `{col: dtype}` mapping |
| `.types()` | Column types + null counts as a DataFrame |
| `.missing()` | Columns with null values (DataFrame) |
| `.duplicates()` | Duplicate row stats as a dict |
| `.summary()` | Descriptive statistics (DataFrame) |
| `.profile()` | Full dataset profile (dict) |
| `.size` | Total cell count |
| `len(df)` | Row count |
| `.to_pandas()` | Raw underlying pandas DataFrame |

### Cleaning

| Method | Description |
|---|---|
| `.clean()` | In-place: duplicates, missing values, column names, dates, whitespace |
| `.clean_report()` | Summary of the last cleaning run (dict) |

### Transform

| Method | Description |
|---|---|
| `.select(*cols)` | New frame with only the given columns (case-insensitive) |
| `.drop(col)` | New frame without a column |
| `.rename(mapping)` | New frame with renamed columns |
| `.sort(by, descending)` | New frame sorted by a column |
| `.filter(expr)` | New frame filtered by a pandas query expression |
| `.group(by)` | `GroupedFrame` for `.sum()` / `.mean()` / etc. |
| `.pivot(index, columns, values)` | Pivot table (new frame) |
| `.join(other, on, how)` | Merge two frames on a shared key |
| `.export(path)` | Write to CSV, XLSX, JSON, or Parquet |

### Visualization

| Method | Description |
|---|---|
| `.bar(x, y, interactive, save)` | Bar chart |
| `.line(x, y, interactive, save)` | Line chart |
| `.scatter(x, y, interactive, save)` | Scatter plot |
| `.hist(column, interactive, save)` | Histogram |
| `.box(x, y, interactive, save)` | Box plot |
| `.violin(x, y, interactive, save)` | Violin plot |
| `.area(x, y, interactive, save)` | Area chart |
| `.pie(labels, values, interactive, save)` | Pie chart |
| `.heatmap(interactive, save)` | Correlation heatmap |
| `.pairplot(save)` | Pairwise scatter matrix |
| `.chart(description)` | Smart chart from plain English |

All methods accept `interactive=True` for Plotly charts (requires `tablofy[viz]`) and `save` to persist the figure.

### Analytics

| Method | Description |
|---|---|
| `.insights()` | Rule-based observations (list of strings) |
| `.stats.describe()` | Descriptive statistics (DataFrame) |
| `.stats.correlation()` | Correlation matrix (DataFrame) |
| `.stats.covariance()` | Covariance matrix (DataFrame) |
| `.stats.outliers(col)` | IQR outlier detection |
| `.stats.mean(col)` / `.median(col)` / `.std(col)` / `.min(col)` / `.max(col)` | Per-column stats |
| `.stats.quantile(col, q)` | Quantile value |
| `.stats.value_counts(col)` | Frequency counts |

### Machine Learning

| Method | Description |
|---|---|
| `.ml.predict(target, features, method, test_size, random_state)` | Train, evaluate, and return model |

### Time Series

| Method | Description |
|---|---|
| `.ts.set_time_index(col)` | Parse & set datetime index (in-place) |
| `.ts.resample(rule, agg)` | Resample by offset alias |
| `.ts.rolling(window, col)` | Rolling mean as a new frame |
| `.ts.detect_trend(col)` | Trend dict: `direction`, `slope`, `strength` |

### SQL

| Method | Description |
|---|---|
| `.sql(query)` | Run DuckDB SQL (table name: `data`) |

### Reports

| Method | Description |
|---|---|
| `.report(path)` | Generate HTML or Excel report |
| `.explore_interactive()` | Jupyter widget dashboard |

---

## What Tablofy Is Not

- **Not a pandas replacement** — access the raw DataFrame anytime with `.to_pandas()`
- **Not a big-data tool** — operates in-memory on a single machine
- **Not a deep-learning framework** — provides lightweight wrappers for quick experiments
- **Not a dashboard server** — reports are static HTML or Excel files
- **Not a database** — SQL runs in-memory against the loaded data only

---

## Contributing

Contributions of all sizes are welcome!

1. Fork the repository on [GitHub](https://github.com/Sheharyar-ans/tablofy)
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Install dev dependencies: `pip install -e ".[dev]"`
4. Run tests: `pytest`
5. Open a pull request

Please open an issue first for substantial changes to discuss the design.

---

## License

[MIT](LICENSE) © Sheharyar Siraj
