# Installation

## Requirements

- Python 3.9 or later
- pip

## Install from PyPI

```bash
pip install tablofy
```

## Verify

```python
import tablofy as tf
print(tf.__version__)
```

## Dependencies

Tablofy installs these libraries automatically:

| Library | Purpose |
|---------|---------|
| pandas | Data manipulation |
| numpy | Numerical operations |
| matplotlib | Static charts |
| seaborn | Statistical charts |
| duckdb | SQL query execution |
| pyarrow | Parquet file support |
| openpyxl | Excel file support |
| jinja2 | HTML report templates |

## Install from source

```bash
git clone https://github.com/your-org/tablofy.git
cd tablofy
pip install -e .
```

## Next steps

See [quickstart.md](quickstart.md) to get started.
