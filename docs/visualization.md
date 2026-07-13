# Charts & Visualization

Tablofy uses **matplotlib** and **seaborn** for static plotting. Every chart method returns a figure object and accepts an optional `save` parameter.

## Bar Chart

```python
data.bar(x="month", y="sales")
data.bar(x="month", y="sales", save="bar.png")
```

## Line Chart

```python
data.line(x="date", y="sales")
```

## Scatter Plot

```python
data.scatter(x="ads", y="sales")
```

## Histogram

```python
data.hist("price")
```

## Box Plot

```python
data.box(x="region", y="sales")
```

## Correlation Heatmap

```python
data.heatmap()
```

Requires at least 2 numeric columns.

## Pairplot

```python
data.pairplot()
```

A matrix of scatter plots for every pair of numeric columns.

## Smart Chart (Plain English)

Describe the chart you want in a simple sentence:

| Phrase | Example | What you get |
|--------|---------|-------------|
| `"<y> by <x>"` | `data.chart("sales by month")` | Bar chart (categorical x) or line chart (numeric x) |
| `"<y> vs <x>"` | `data.chart("profit vs ad_spend")` | Scatter plot |

Column names are matched case-insensitively.

## Saving

Every chart method accepts `save="path.png"`:

```python
data.bar(x="month", y="sales", save="charts/sales_by_month.png")
data.heatmap(save="charts/correlation.png")
data.chart("sales by month", save="charts/smart_chart.png")
```
