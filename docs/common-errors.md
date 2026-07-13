# Common Errors

Tablofy uses clear exception types to help you diagnose problems quickly.

## `TablofyDataError`

The dataset is empty or the operation produced no data.

```python
tf.TablofyFrame(pd.DataFrame())       # Error: cannot create from empty dataset
data.filter("sales > 999999")         # Error: filter returned no rows
data.sql("")                          # Error: SQL query cannot be empty
data.sql("DROP TABLE data")           # Error: only read-only queries allowed
```

**Fix:** Check that your file has data, relax your filter condition, or use a read-only SQL statement.

## `TablofyColumnError`

A required column does not exist.

```python
data.select("bad_column")             # Error: column not found
data.sort("missing")                  # Error: column not found
data.stats.outliers("nope")           # Error: column not found
data.chart("sales by flurbo")         # Error: column 'flurbo' not found
```

**Fix:** Use `data.columns()` to see available column names.

## `TablofyFileError`

A file could not be found, read, or its format is unsupported.

```python
tf.load("data.txt")                   # Error: unsupported format
data.export("out.pdf")                # Error: unsupported export format
data.report("out.pdf")                # Error: unsupported report format
```

**Fix:** Use a supported extension.

**Loading:** `.csv`, `.xlsx`, `.xls`, `.json`, `.parquet`
**Export:** `.csv`, `.xlsx`, `.json`, `.parquet`
**Reports:** `.html`, `.xlsx`

## `TablofyChartError`

A chart could not be created.

```python
data.heatmap()                        # Error: need at least 2 numeric columns
data.pairplot()                       # Error: need at least 2 numeric columns
```

**Fix:** Ensure you have enough numeric columns for the chart type.

## `TablofyParseError`

The smart chart parser could not understand your description.

```python
data.chart("something random")        # Error: could not parse description
```

**Fix:** Use the pattern `"<y> by <x>"` for bar/line charts or `"<y> vs <x>"` for scatter plots.

## SQL errors

### Unsupported statement

```python
data.sql("DROP TABLE data")           # Error: only SELECT/WITH/DESCRIBE/EXPLAIN
```

**Fix:** Use read-only statements.

### Execution error

```python
data.sql("SELECT * FROM bad_table")   # Error: table not found
```

**Fix:** The table is always named `data`. Use `SELECT * FROM data`.
