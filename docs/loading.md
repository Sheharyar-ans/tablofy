# Loading Data

## From a file

```python
import tablofy as tf

data = tf.load("data.csv")
```

The `load()` function returns a `TablofyFrame`. The format is detected automatically from the file extension.

### Supported formats

| Extension | Format |
|-----------|--------|
| `.csv` | Comma-separated values |
| `.xlsx` | Excel workbook |
| `.xls` | Excel 97-2003 workbook |
| `.json` | JSON array of objects |
| `.parquet` | Apache Parquet |

### CSV options

```python
data = tf.load("data.csv", sep=";")           # custom delimiter
data = tf.load("data.csv", encoding="latin-1")
```

Any keyword argument beyond the file path is forwarded to `pandas.read_csv()`,
`pandas.read_excel()`, etc.

## From a pandas DataFrame

```python
import pandas as pd
from tablofy import TablofyFrame

df = pd.DataFrame({"name": ["Alice"], "sales": [100]})
data = TablofyFrame(df)
```

## Empty files

Tablofy raises `TablofyDataError` if you try to load an empty file or create
a `TablofyFrame` from an empty DataFrame.

## Unsupported formats

Passing a `.pdf`, `.txt`, or other unsupported file raises
`TablofyFileError` with a clear message.

## Exporting

```python
data.export("clean.csv")
data.export("clean.xlsx")
data.export("clean.json")
data.export("clean.parquet")
```

The format is inferred from the extension, same as loading.
