# SQL Queries

Tablofy uses **DuckDB** to run SQL queries directly on a `TablofyFrame`.

The frame is registered as the table `data` inside the query.

```python
result = data.sql("SELECT * FROM data")
```

The result is always a `TablofyFrame`, so you can chain:

```python
result = data.sql("SELECT * FROM data WHERE sales > 100")
result.chart("sales by month")
```

## Examples

### Filtering

```python
data.sql("SELECT * FROM data WHERE sales > 100")
```

### Aggregation

```python
data.sql("""
    SELECT region, SUM(sales) AS total
    FROM data
    GROUP BY region
""")
```

### Sorting

```python
data.sql("SELECT * FROM data ORDER BY sales DESC")
```

### CTEs (WITH clause)

```python
data.sql("""
    WITH filtered AS (
        SELECT * FROM data WHERE sales > 100
    )
    SELECT region, COUNT(*) AS cnt
    FROM filtered
    GROUP BY region
""")
```

## Safety

Only read-only statements are permitted:

- `SELECT`
- `WITH` (common table expressions)
- `DESCRIBE`
- `EXPLAIN`
- `SHOW`
- `PRAGMA`

Write statements (`INSERT`, `UPDATE`, `DELETE`, `DROP`, `CREATE`, etc.) are rejected with `TablofyDataError`.
