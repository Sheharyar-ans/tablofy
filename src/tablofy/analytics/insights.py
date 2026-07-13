"""Rule-based insight generation."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tablofy.core.frame import TablofyFrame


class Insights:
    """Generates deterministic, rule-based observations about a dataset."""

    def __init__(self, frame: TablofyFrame) -> None:
        self._frame = frame
        self._df = frame._df

    def generate(self) -> list[str]:
        """Return a list of human-readable insight strings.

        Checks performed
        -----------------
        - Dataset dimensions
        - Missing values
        - Duplicate rows
        - Strong correlations
        - High-cardinality columns
        - Low-cardinality categorical columns
        - Highest/lowest numeric values
        - Outlier hints
        """
        insights: list[str] = []
        df = self._df

        rows, cols = df.shape
        insights.append(f"Dataset has {rows} rows and {cols} columns.")

        # Missing values
        missing_counts = df.isna().sum()
        total_missing = int(missing_counts.sum())
        if total_missing:
            pct = total_missing / df.size * 100
            insights.append(
                f"Found {total_missing} missing cell(s) ({pct:.1f}% of data)."
            )
            cols_with_missing = [c for c in df.columns if missing_counts[c] > 0]
            insights.append(
                f"Columns with missing values: {cols_with_missing}."
            )
        else:
            insights.append("No missing values detected.")

        # Duplicate rows
        dup_count = int(df.duplicated().sum())
        if dup_count:
            dup_pct = dup_count / rows * 100
            insights.append(
                f"Found {dup_count} duplicate row(s) ({dup_pct:.1f}% of rows)."
            )
        else:
            insights.append("No duplicate rows found.")

        # Strong correlations
        numeric = df.select_dtypes(include="number")
        if numeric.shape[1] >= 2:
            corr = numeric.corr().abs()
            strong: list[str] = []
            for i in range(len(corr.columns)):
                for j in range(i + 1, len(corr.columns)):
                    val = corr.iloc[i, j]
                    if val >= 0.7:
                        strong.append(
                            f"{corr.columns[i]} — {corr.columns[j]} "
                            f"(r = {corr.iloc[i, j]:.2f})"
                        )
            if strong:
                insights.append(
                    f"Strong correlations detected ({len(strong)}): "
                    f"{'; '.join(strong)}."
                )
            else:
                insights.append(
                    "No strong correlations (|r| >= 0.7) found between numeric columns."
                )

        # High-cardinality columns
        high_card = [
            c for c in df.columns
            if df[c].nunique() > 50 and df[c].nunique() == len(df)
        ]
        if high_card:
            insights.append(
                f"High-cardinality columns (unique ID-like): {high_card}."
            )

        # Low-cardinality categorical columns
        obj_cols = df.select_dtypes(include=["object", "category"]).columns
        low_card = [c for c in obj_cols if 2 <= df[c].nunique() <= 10]
        if low_card:
            insights.append(
                f"Low-cardinality categorical columns ({len(low_card)}): "
                f"{low_card}."
            )

        # Highest / lowest numeric
        if numeric.shape[1] >= 1:
            for col in numeric.columns:
                max_val = df[col].max()
                min_val = df[col].min()
                insights.append(
                    f"{col}: min = {min_val}, max = {max_val}."
                )

        # Outlier hints (IQR-based)
        if numeric.shape[1] >= 1:
            for col in numeric.columns:
                q1 = df[col].quantile(0.25)
                q3 = df[col].quantile(0.75)
                iqr = q3 - q1
                lower = q1 - 1.5 * iqr
                upper = q3 + 1.5 * iqr
                outlier_count = int(((df[col] < lower) | (df[col] > upper)).sum())
                if outlier_count:
                    pct = outlier_count / rows * 100
                    insights.append(
                        f"{col}: {outlier_count} potential outlier(s) "
                        f"({pct:.1f}% of rows)."
                    )

        return insights
