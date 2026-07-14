# Changelog

## 2.1.0 (2026-07-14)

- Interactive Plotly charts (``interactive=True`` on all chart methods).
- Three new chart types: area, pie, violin.
- Global theme/style system (``tf.set_theme()``) with 4 built-in themes.
- Time-series helpers (``data.ts``): set_time_index, resample, rolling, detect_trend.
- Lazy-loaded namespaces for ML (``data.ml``), web scraping (``data.scrape``), advanced stats (``data.stats``).
- Jupyter Notebook widget explorer (``data.explore_interactive()``).
- Optional dependency extras (``[ml]``, ``[viz]``, ``[widgets]``, ``[stats]``, ``[scraping]``, ``[fast]``, ``[dl]``, ``[all]``).
- Delegation-based ``__getattr__`` for native pandas method access with automatic TablofyFrame wrapping.
- Robust HTML report engine using ``importlib.resources`` and NaN sanitisation.

## 2.0.0 (2026-07-14)

- Stable release of Tablofy v2.
- Data loading for CSV, Excel, JSON, and Parquet.
- Exploration, cleaning, transformations, visualization, SQL, analytics, and reporting.
- Rule-based insights.
- HTML and Excel reports.

## 1.0.0 (2026-07-14)

- Stable release of Tablofy v1.
- Data loading support for CSV, XLSX, XLS, JSON, and Parquet.
- Exploration methods: preview, head, shape, columns, types, missing, duplicates, summary, profile.
- Cleaning methods: clean and clean_report.
- Transform methods: select, drop, rename, sort, filter, group, pivot, join, export.
- Visualization methods: bar, line, scatter, hist, box, heatmap, pairplot, chart.
- Rule-based insights.
- Stats helpers.
- DuckDB SQL support.
- HTML and Excel reporting.

## 1.0.0-alpha (2026-07-13)

- Initial pre-release.
- Data loading: CSV, Excel, JSON, Parquet.
- Data cleaning: duplicates, missing values, column names, dates, text.
- Data exploration: preview, shape, columns, types, missing, duplicates, summary, profile.
- Transformation: select, drop, rename, sort, filter, group, pivot, join, export.
- Visualization: bar, line, scatter, hist, box, heatmap, pairplot, smart chart.
- Analytics: rule-based insights, descriptive stats, correlation, covariance, outlier detection.
- SQL queries via DuckDB.
- HTML and Excel reports.
