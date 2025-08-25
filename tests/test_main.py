import sys
import pathlib
import io
import polars as pl
from data_ingestion import convert_dataframe_to_parquet
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

def test_convert_dataframe_to_parquet_roundtrip():
    original_df = pl.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})

    parquet_buffer = convert_dataframe_to_parquet(original_df)

    assert parquet_buffer is not None, "Expected a BytesIO buffer, got None"
    assert isinstance(parquet_buffer, io.BytesIO), "Result should be an in-memory BytesIO buffer"

    parquet_buffer.seek(0)
    roundtrip_df = pl.read_parquet(parquet_buffer)

    # Compare via to_dicts() for compatibility with installed Polars version
    assert roundtrip_df.to_dicts() == original_df.to_dicts(), "Round-tripped DataFrame should equal the original"


def test_convert_dataframe_to_parquet_handles_exceptions():
    """If the object's write_parquet raises, the function should return None."""

    class BadWriter:
        def write_parquet(self, buffer):
            raise ValueError("boom")

    bad_writer = BadWriter()
    conversion_result = convert_dataframe_to_parquet(bad_writer)
    assert conversion_result is None
