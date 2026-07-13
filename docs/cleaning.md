# Cleaning

```python
data.clean()
```

The `clean()` method runs a full suite of cleaning steps with sensible defaults.
It modifies the data **in place** and returns `self` so you can chain it.

## What it does by default

| Task | Default | What happens |
|------|---------|-------------|
| Remove duplicates | `True` | Duplicate rows are dropped |
| Fill missing values | `"smart"` | Numeric → median; text → mode (or `""` if none) |
| Normalise column names | `"snake_case"` | `"First Name"` → `"first_name"`, `"Sales (2024)"` → `"sales_2024"` |
| Parse dates | `True` | Object columns that look like dates are converted to `datetime` |
| Strip whitespace | `True` | Text values are trimmed; fully empty columns are dropped |

## Customising

```python
data.clean(
    duplicates=False,            # keep duplicate rows
    missing="off",               # don't fill missing values
    columns=False,               # keep original column names
    dates=False,                 # don't parse dates
    text=False,                  # don't strip whitespace
)
```

Or fill missing values manually:

```python
data.clean(missing={"age": 30, "city": "Unknown"})
```

## Cleaning report

After cleaning, you can see what was done:

```python
report = data.clean_report()
print(report["summary_text"])
# → "Cleaning completed: 3 action(s) performed."
```

The report is also included in HTML and Excel reports automatically.

## Note on mutation

`clean()` modifies the original data in place. Transform methods like `select()`,
`drop()`, and `filter()` return a new frame and do not modify the original.

```python
small = data.select("name", "sales")   # original is unchanged
```
