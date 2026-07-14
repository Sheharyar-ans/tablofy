"""Lazy-loaded ML wrapper (scikit-learn)."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from tablofy.core.frame import TablofyFrame


class MLWrapper:
    """Entry point for ML operations on a TablofyFrame.

    Accessed via ``data.ml``.

    Requires ``tablofy[ml]`` (scikit-learn).
    """

    def __init__(self, frame: TablofyFrame) -> None:
        self._frame = frame
        self._df = frame._df
        self._model = None

    def _check_imports(self) -> None:
        try:
            import sklearn  # noqa: F401
        except ImportError:
            raise ImportError(
                "scikit-learn is required for ML features.\n"
                "  pip install tablofy[ml]"
            ) from None

    def predict(
        self,
        target: str,
        features: list,
        method: str = "classification",
        test_size: float = 0.2,
        random_state: int = 42,
    ) -> Any:
        """Train a model and print evaluation metrics.

        Parameters
        ----------
        target : str
            Name of the target column.
        features : list
            Feature column names.
        method : str
            ``"classification"`` (RandomForestClassifier) or
            ``"regression"`` (LinearRegression).
        test_size : float
            Fraction of data to hold out for testing (default 0.2).
        random_state : int
            Random seed for reproducibility (default 42).

        Returns
        -------
        Trained scikit-learn estimator.
        """
        self._check_imports()
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import StandardScaler
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.linear_model import LinearRegression
        from sklearn.metrics import accuracy_score, classification_report, mean_squared_error, r2_score

        df = self._df.copy()

        if target not in df.columns:
            raise ValueError(f"Target column '{target}' not found in data.")

        for col in features:
            if col not in df.columns:
                raise ValueError(f"Feature column '{col}' not found in data.")

        X = df[features]
        y = df[target]

        X = X.fillna(X.mean(numeric_only=True))

        if y.dtype == "object":
            y = y.fillna(y.mode().iloc[0] if not y.mode().empty else "unknown")
        else:
            y = y.fillna(y.mean())

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        if method == "classification":
            model = RandomForestClassifier(random_state=random_state)
        elif method == "regression":
            model = LinearRegression()
        else:
            raise ValueError(f"Unknown method '{method}'. Use 'classification' or 'regression'.")

        model.fit(X_train_scaled, y_train)
        predictions = model.predict(X_test_scaled)

        print(f"\n{'='*50}")
        print(f"Model type: {method}")
        print(f"Target column: {target}")
        print(f"Features ({len(features)}): {features}")
        print(f"Train size: {len(X_train)}  |  Test size: {len(X_test)}")
        print("-" * 50)

        if method == "classification":
            acc = accuracy_score(y_test, predictions)
            print(f"Accuracy: {acc:.4f}")
            print(classification_report(y_test, predictions))
        else:
            mse = mean_squared_error(y_test, predictions)
            r2 = r2_score(y_test, predictions)
            print(f"Mean Squared Error: {mse:.4f}")
            print(f"R² Score: {r2:.4f}")

        print(f"{'='*50}\n")

        self._model = model
        return model
