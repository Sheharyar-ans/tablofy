<p align="center">
  <h1 align="center">⚡ TABLOFY (v2.1.3) ⚡</h1>
  <p align="center"><em>One import to rule them all — zero-boilerplate data analytics for Python.</em></p>
</p>

<p align="center">
  <a href="https://pypi.org/project/tablofy/"><img src="https://img.shields.io/pypi/v/tablofy?label=version&color=blue&logo=python" alt="Version 2.1.3"></a>
  <a href="LICENSE"><img src="https://img.shields.io/pypi/l/tablofy?color=green" alt="MIT License"></a>
  <a href="https://pypi.org/project/tablofy/"><img src="https://img.shields.io/pypi/pyversions/tablofy?color=orange" alt="Python 3.8+"></a>
  <a href="https://pypi.org/project/tablofy/"><img src="https://img.shields.io/badge/environment-notebook%20%7C%20script-lightgrey" alt="Notebook & Script"></a>
</p>

---

## 📖 Table of Contents

- [Why Tablofy?](#-why-tablofy)
- [The Comparison](#-the-comparison)
- [Installation](#-installation)
- [Quickstart](#-quickstart)
- [How to Display & Render Visuals](#-how-to-display--render-visuals)
- [Unified Engine Shortcuts](#-unified-engine-shortcuts)
- [Subscriptable Bracket Support](#-subscriptable-bracket-support)
- [Auto-Cleaning Pipeline](#-auto-cleaning-pipeline)
- [Zero-Boilerplate ML Predictions](#-zero-boilerplate-ml-predictions)
- [Time-Series Engine](#-time-series-engine)
- [Aesthetic Themes](#-aesthetic-themes)
- [API Overview](#-api-overview)
- [License](#-license)

---

## 🎯 Why Tablofy?

Stop writing the same 10 imports at the top of every notebook. Tablofy wraps **pandas, numpy, matplotlib, seaborn, Plotly, scikit-learn, statsmodels, and DuckDB** behind a single, consistent API.

- **One import.** `import tablofy as tf` — that's it.
- **Unified shortcuts.** `tf.pd`, `tf.np`, and `tf.show()` available immediately.
- **Bracket selection.** `df['Column']` returns a pandas Series natively.
- **Zero-boilerplate ML.** `df.ml.predict(target, features, method="classification")` — no manual train/test split, scaling, or metric imports.
- **Rolling time-series.** `df.ts.rolling(window=7, col="sales")` returns a fresh `TablofyFrame`.

---

## ⚖️ The Comparison

| Aspect | The Standard Python Way | The Tablofy Way |
|---|---|---|
| **Imports** | `import pandas as pd`<br>`import numpy as np`<br>`import matplotlib.pyplot as plt`<br>`import seaborn as sns`<br>`from sklearn.model_selection import train_test_split`<br>`from sklearn.preprocessing import StandardScaler`<br>`from sklearn.ensemble import RandomForestClassifier`<br>`from sklearn.metrics import accuracy_score` | `import tablofy as tf` |
| **Load CSV** | `pd.read_csv("data.csv")` | `tf.load("data.csv")` |
| **Clean** | 5–10 lines of manual `.fillna()`, `.drop_duplicates()`, column rename logic | `df.clean()` |
| **Bar chart** | `plt.figure(figsize=(8,5))`<br>`sns.barplot(data=df, x="a", y="b")`<br>`plt.title("...")`<br>`plt.show()` | `df.bar(x="a", y="b")` |
| **ML pipeline** | `X_train, X_test, y_train, y_test = train_test_split(...)`<br>`scaler = StandardScaler()`<br>`X_train = scaler.fit_transform(X_train)`<br>`X_test = scaler.transform(X_test)`<br>`model = RandomForestClassifier()`<br>`model.fit(X_train, y_train)`<br>`preds = model.predict(X_test)`<br>`print(accuracy_score(y_test, preds))` | `model = df.ml.predict(target, features, method="classification")` |
| **Time-series rolling** | `df['sales'].rolling(window=7).mean()`<br>(returns a raw Series) | `df.ts.rolling(window=7, col="sales")`<br>(returns a `TablofyFrame`) |
| **HTML report** | Manual Jinja2 template + custom CSS | `df.report("report.html")` |

---

## 📦 Installation

```bash
pip install tablofy
```

Requires Python 3.8 or later.

### Optional extras (install individually for a leaner setup)

| Command | What you get |
|---|---|
| `pip install tablofy` | Core: pandas, numpy, matplotlib, seaborn, DuckDB, Jinja2 |
| `pip install "tablofy[viz]"` | Interactive Plotly charts (`interactive=True`) |
| `pip install "tablofy[ml]"` | Scikit-learn ML pipeline (`df.ml.predict`) |
| `pip install "tablofy[stats]"` | SciPy / Statsmodels advanced statistics |
| `pip install "tablofy[widgets]"` | Jupyter Notebook widget explorer |
| `pip install "tablofy[scraping]"` | Web scraping with BeautifulSoup & Requests |
| `pip install "tablofy[fast]"` | Polars / PyArrow for large datasets |
| `pip install "tablofy[dl]"` | PyTorch / TensorFlow deep learning |

---

## 🚀 Quickstart

A complete end-to-end pipeline in 10 lines — no separate imports required.

```python
import tablofy as tf

# 1. Load local dataset
df = tf.load("titanic_dataset.csv")

# 2. Subset columns with case-insensitive smart selection
df = df.select("Pclass", "Sex", "Age", "Fare", "Survived")

# 3. Auto-clean: fill missing values, snake_case columns, strip whitespace
df.clean()

# 4. Bracket selection returns a native pandas Series
print(df['Survived'].value_counts())

# 5. Train and evaluate a classifier
model = df.ml.predict(
    target="Survived",
    features=["Pclass", "Age", "Fare"],
    method="classification",
)
print(f"Accuracy: {model.score.__name__ if hasattr(model, 'score') else 'N/A'}")
```

> That's it. No `import pandas as pd`. No `train_test_split`. No `StandardScaler`. No `accuracy_score`.

---

## 🎨 How to Display & Render Visuals

Beginners often hit rendering issues in notebooks because matplotlib figures don't always show automatically. Tablofy gives you **three reliable ways** to display visuals.

### Method 1: The Interactive Way (Recommended)

Set `interactive=True` to use Plotly, which renders instantly in any notebook environment without any `show()` command.

```python
import tablofy as tf

df = tf.load("titanic_dataset.csv")

# Interactive charts display immediately — no show() needed
df.bar(x="Sex", y="Fare", interactive=True)
df.scatter(x="Age", y="Fare", interactive=True)
df.violin(x="Sex", y="Age", interactive=True)
```

> Plotly figures are self-rendering in Jupyter Notebook, Jupyter Lab, VS Code, and Google Colab.

### Method 2: The Variable Notebook Mode

Store the plot in a variable and write it on the last line of the cell. Jupyter will automatically render the matplotlib figure.

```python
import tablofy as tf

df = tf.load("titanic_dataset.csv")

fig = df.box(x="Pclass", y="Age")
fig   # ← put the variable name on the last line of the cell
```

> This works because Jupyter displays the last expression in a cell. It also works with `fig.show()` in matplotlib.

### Method 3: The Script Mode

For standalone `.py` scripts, use Tablofy's global `tf.show()` wrapper to display all active figures at once.

```python
import tablofy as tf

df = tf.load("titanic_dataset.csv")

df.bar(x="Pclass", y="Fare")
df.hist(column="Age")
df.heatmap()

# Display everything in one call
tf.show()
```

> `tf.show()` calls `matplotlib.pyplot.show()` internally — it's a unified shortcut so you never need `import matplotlib.pyplot as plt`.

---

## 🔧 Unified Engine Shortcuts

Tablofy exposes **pandas** and **numpy** directly on the `tf` namespace so you never need to import them separately.

```python
import tablofy as tf

# pandas — ready to use
print(tf.pd.DataFrame({"col": [1, 2, 3]}))

# numpy — ready to use
print(tf.np.array([10, 20, 30]))

# Display all figures (calls plt.show() internally)
tf.show()
```

> `tf.pd` and `tf.np` gracefully fall back to `None` if the underlying library is missing, so your code never crashes at import time.

---

## 📎 Subscriptable Bracket Support

`TablofyFrame` supports **native Python square-bracket subscripting** — just like a regular pandas DataFrame.

```python
import tablofy as tf

df = tf.load("titanic_dataset.csv")

# String key → returns a native pandas Series
ages = df['Age']
print(type(ages))             # <class 'pandas.core.series.Series'>
print(ages.unique())          # chaining works out of the box

# List of keys → returns a new TablofyFrame
subset = df[['Pclass', 'Fare', 'Age']]
print(type(subset))           # <class 'tablofy.core.frame.TablofyFrame'>
print(subset.preview())
```

> This means `df['Pclass'].unique()`, `df['Age'].mean()`, and `df[['A','B']].clean()` all work naturally without any manual unwrapping.

---

## 🧼 Auto-Cleaning Pipeline

```python
import tablofy as tf

df = tf.load("titanic_dataset.csv")

# One-shot cleaning — everything in a single call
df.clean()
```

**What `df.clean()` does automatically:**

| Action | Default | Effect |
|---|---|---|
| Remove duplicates | `True` | Drops fully duplicate rows |
| Fill missing values | `"smart"` | Numeric → median; Text → mode |
| Normalise column names | `"snake_case"` | `"PassengerId"` → `"passenger_id"` |
| Parse dates | `True` | Detects and converts date-like columns |
| Strip whitespace | `True` | Trims leading/trailing spaces from text |

```python
# Get a human-readable report of what was fixed
report = df.clean_report()
print(report['summary_text'])
```

> The `clean_report()` method logs every action taken so you always know what changed.

---

## 🤖 Zero-Boilerplate ML Predictions

No manual imports. No boilerplate. Just pick your target, features, and method.

```python
import tablofy as tf

df = tf.load("titanic_dataset.csv")

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

### What happens under the hood

| Step | Description |
|---|---|
| 1. Imputation | Numerical NaNs filled with column means |
| 2. Train/Test split | `test_size=0.2` (configurable) |
| 3. Scaling | Features scaled with `StandardScaler` |
| 4. Training | `RandomForestClassifier` or `LinearRegression` |
| 5. Evaluation | Accuracy + classification report (or MSE + R²) printed to terminal |
| 6. Return | Trained estimator object returned |

### Example output (classification)

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

---

## ⏱ Time-Series Engine

```python
import tablofy as tf

df = tf.load("sales_data.csv")

# Convert a date column to datetime and set it as the index
df.ts.set_time_index("date")

# Rolling mean — returns a new TablofyFrame
rolling_result = df.ts.rolling(window=7, col="revenue")
print(type(rolling_result))   # <class 'tablofy.core.frame.TablofyFrame'>
print(rolling_result.preview())

# Resample to weekly sums
weekly = df.ts.resample(rule="W", agg="sum")

# Detect trend direction
trend = df.ts.detect_trend("revenue")
# → {"direction": "upward", "slope": 40.0, "strength": "strong"}
```

> `df.ts.rolling(window, col)` returns a **new** `TablofyFrame` (not a raw Series), so you can chain further operations on it.

---

## 🎭 Aesthetic Themes

Apply a consistent visual style to **all** charts — both static (matplotlib/seaborn) and interactive (Plotly) — with a single call.

```python
import tablofy as tf

tf.set_theme("dark")       # Dark background with neon accents
tf.set_theme("modern")     # Clean, minimal, sans-serif style
tf.set_theme("pastel")     # Soft, bright, friendly colours
tf.set_theme("classic")    # Academic style, serif font, no grid
tf.set_theme("default")    # Reset to matplotlib/seaborn defaults

# Custom colour palette
tf.set_theme("modern", palette=["#ff6b6b", "#4ecdc4", "#45b7d1"])
```

> Themes propagate to matplotlib rcParams, seaborn `set_palette()`, and Plotly `template` simultaneously.

---

## 📋 API Overview

### Loading

| Method | Description |
|---|---|
| `tf.load(path)` | Load any supported file (auto-detects format) |
| `TablofyFrame(df, name)` | Wrap an existing pandas DataFrame |

### Exploration

| Method | Description |
|---|---|
| `.preview(n=5)` / `.head(n=5)` | First `n` rows |
| `.shape()` | `{"rows": N, "columns": M}` |
| `.columns()` | List of column names |
| `.dtypes` | `{col: dtype}` as a dict |
| `.types()` | Column types + null counts (DataFrame) |
| `.missing()` | Columns with null values (DataFrame) |
| `.duplicates()` | Duplicate row stats (dict) |
| `.summary()` | Descriptive statistics (DataFrame) |
| `.profile()` | Full dataset profile (dict) |
| `.size` | Total cell count |
| `len(df)` | Row count |
| `.to_pandas()` | Raw underlying pandas DataFrame |

### Cleaning

| Method | Description |
|---|---|
| `.clean()` | In-place: duplicates, missing, column names, dates, whitespace |
| `.clean_report()` | Summary of the last cleaning run (dict) |

### Transform

| Method | Description |
|---|---|
| `.select(*cols)` | New frame with given columns (case-insensitive) |
| `.drop(col)` | New frame without a column |
| `.rename(mapping)` | New frame with renamed columns |
| `.sort(by, descending)` | New frame sorted by a column |
| `.filter(expr)` | New frame filtered by a pandas query |
| `.group(by)` | `GroupedFrame` for aggregation |
| `.pivot(index, columns, values)` | Pivot table |
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

All methods accept `interactive=True` for Plotly charts (requires `tablofy[viz]`) and `save` to persist figures.

### Machine Learning

| Method | Description |
|---|---|
| `.ml.predict(target, features, method, test_size, random_state)` | Train, evaluate, and return model |

### Time Series

| Method | Description |
|---|---|
| `.ts.set_time_index(col)` | Parse & set datetime index (in-place) |
| `.ts.resample(rule, agg)` | Resample by offset alias |
| `.ts.rolling(window, col)` | Rolling mean as a new `TablofyFrame` |
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

## 📄 License

[MIT](LICENSE) © Sheharyar Siraj
