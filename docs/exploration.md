# Exploration

Once you've loaded data, you'll want to understand its structure. Tablofy provides several methods for this.

## preview()

See the first rows:

```python
data.preview()       # first 5 rows
data.preview(10)     # first 10 rows
```

Returns a pandas DataFrame.

## shape()

Row and column counts:

```python
s = data.shape()
print(s["rows"], s["columns"])
```

## columns()

Column names:

```python
print(data.columns())
# → ["date", "region", "product", "sales", "profit"]
```

## types()

Column types and null counts:

```python
print(data.types())
#   column  dtype    non_null  nulls  null_pct
# 0  date   object          5      0       0.0
# 1  region object          5      0       0.0
```

## missing()

Columns with missing values:

```python
print(data.missing())
#   column   missing  percent
# 0  sales         1     20.0
```

Only columns with at least one null are shown.

## duplicates()

Duplicate row statistics:

```python
print(data.duplicates())
# → {"count": 3, "percent": 1.5}
```

## summary()

Descriptive statistics for all columns:

```python
print(data.summary())
#         sales      profit
# count     5.0     5.000000
# mean    200.0    50.000000
# std      50.0    10.000000
# min     100.0    30.000000
# 25%     150.0    40.000000
# 50%     200.0    50.000000
# 75%     250.0    60.000000
# max     300.0    80.000000
```

## profile()

A full dataset profile as a dictionary:

```python
p = data.profile()
print(p["rows"])                  # row count
print(p["columns"])               # column count
print(p["missing_cells"])         # total missing cells
print(p["missing_percent"])       # percentage of missing cells
print(p["duplicate_rows"])        # number of duplicate rows
print(p["numeric_columns"])       # list of numeric column names
print(p["text_columns"])          # list of text column names
print(p["date_columns"])          # list of date column names
print(p["categorical_columns"])   # list of categorical column names
print(p["memory_usage"])          # memory usage in bytes
```

## dtypes property

Column-to-dtype mapping:

```python
for col, dtype in data.dtypes.items():
    print(f"{col}: {dtype}")
```

## size property

Total cell count:

```python
print(data.size)    # rows × columns
```

## len()

Row count:

```python
print(len(data))
```
