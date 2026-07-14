"""Tests for tf.load() and top-level exports."""

import pandas as pd
import pytest

import tablofy as tf


class TestTopLevelExports:
    def test_import_as_tf(self):
        assert tf.__version__ == "2.1.3"

    def test_load_exists(self):
        assert callable(tf.load)

    def test_tablofy_frame_exists(self):
        assert tf.TablofyFrame is not None

    def test_tablofy_error_exists(self):
        assert issubclass(tf.TablofyError, Exception)

    def test_tablofy_file_error_exists(self):
        assert issubclass(tf.TablofyFileError, tf.TablofyError)

    def test_tablofy_column_error_exists(self):
        assert issubclass(tf.TablofyColumnError, tf.TablofyError)

    def test_tablofy_data_error_exists(self):
        assert issubclass(tf.TablofyDataError, tf.TablofyError)

    def test_column_not_found_error_alias(self):
        assert tf.ColumnNotFoundError is tf.TablofyColumnError

    def test_empty_table_error_alias(self):
        assert tf.EmptyTableError is tf.TablofyDataError

    def test_file_format_error_alias(self):
        assert tf.FileFormatError is tf.TablofyFileError

    def test_all_exports(self):
        expected = {
            "TablofyFrame", "load",
            "TablofyError", "TablofyFileError",
            "TablofyColumnError", "TablofyDataError",
            "ColumnNotFoundError", "EmptyTableError", "FileFormatError",
        }
        assert expected.issubset(set(dir(tf)))


class TestLoad:
    @pytest.fixture
    def sample_df(self):
        return pd.DataFrame({
            "name": ["Alice", "Bob"],
            "age": [25, 30],
            "salary": [50000.0, 60000.0],
        })

    def test_load_csv(self, tmp_path, sample_df):
        path = tmp_path / "data.csv"
        sample_df.to_csv(path, index=False)
        result = tf.load(str(path))
        assert result.name == "data"
        assert isinstance(result, tf.TablofyFrame)

    def test_load_excel(self, tmp_path, sample_df):
        path = tmp_path / "data.xlsx"
        sample_df.to_excel(path, index=False)
        result = tf.load(str(path))
        assert result.name == "data"

    def test_load_json(self, tmp_path, sample_df):
        path = tmp_path / "data.json"
        sample_df.to_json(path, orient="records")
        result = tf.load(str(path))
        assert result.name == "data"

    def test_load_parquet(self, tmp_path, sample_df):
        path = tmp_path / "data.parquet"
        sample_df.to_parquet(path, index=False)
        result = tf.load(str(path))
        assert result.name == "data"

    def test_invalid_file_path(self):
        with pytest.raises(tf.TablofyFileError):
            tf.load("nonexistent_file.csv")

    def test_unsupported_format(self, tmp_path):
        path = tmp_path / "data.txt"
        path.write_text("hello")
        with pytest.raises(tf.TablofyFileError):
            tf.load(str(path))

    def test_empty_csv(self, tmp_path):
        path = tmp_path / "empty.csv"
        path.write_text("a,b,c\n")
        with pytest.raises(tf.TablofyDataError):
            tf.load(str(path))

    def test_load_returns_tablofy_frame(self, tmp_path, sample_df):
        path = tmp_path / "data.csv"
        sample_df.to_csv(path, index=False)
        result = tf.load(str(path))
        from tablofy import TablofyFrame
        assert isinstance(result, TablofyFrame)

    def test_load_passes_kwargs_to_csv(self, tmp_path):
        path = tmp_path / "data.csv"
        path.write_text("a|b\n1|2\n3|4\n")
        result = tf.load(str(path), sep="|")
        assert result.name == "data"
