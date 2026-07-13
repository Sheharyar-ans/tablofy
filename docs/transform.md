# Transform

All transformation methods return a **new** `TablofyFrame` — the original is unchanged.

## Select columns

```python
result = data.select("name", "sales")
```

## Drop a column

```python
result = data.drop("age")
```

## Rename columns

```python
result = data.rename({"name": "full_name", "region": "r"})
```

## Sort

```python
result = data.sort("sales")                   # ascending (default)
result = data.sort("sales", descending=True)  # descending
```

## Filter rows

Uses pandas-compatible expressions. Column names are validated before execution.

```python
result = data.filter("sales > 1000")
result = data.filter("region == 'North'")
result = data.filter("sales > 500 & region == 'North'")
```

## Group and aggregate

```python
data.group("region").sum("sales")
data.group("region").mean("sales")
data.group("region").sum()           # all numeric columns
```

## Pivot table

```python
data.pivot(index="region", columns="name", values="sales", aggfunc="mean")
```

## Join

```python
data.join(other_frame, on="id")
data.join(other_frame, on="id", how="left")      # inner, left, right, outer
```

## Export

```python
data.export("clean.csv")
data.export("clean.xlsx")
data.export("clean.json")
data.export("clean.parquet")
```

## Chaining

All methods return a `TablofyFrame`, so you can build pipelines:

```python
result = (
    data
    .drop("id")
    .filter("sales > 100")
    .group("region").sum("sales")
    .sort("sales", descending=True)
)
```
