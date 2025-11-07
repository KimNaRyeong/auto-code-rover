def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    try:
        import xarray as xr
        da = xr.DataArray([[[1]]], dims=["a", "b", "c"]).stack(ab=["a", "b"])
        # Attempt to convert to series, expecting a MultiIndex with the names a, b, c.
        series = da.to_series()
        # Additionally, attempt to convert to a DataFrame
        df = da.to_dataframe("A")

        # If either operation fails to produce the right index, we raise an AssertionError.
        assert 'ab' in series.index.names, "Expected MultiIndex with 'ab' but got different index names."
        assert 'ab' in df.index.names, "Expected MultiIndex with 'ab' but got different index names."
        assert 'c' in df.index.names, "Expected 'c' in DataFrame index names."

        print("Successfully converted DataArray to Series and DataFrame.")
    
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("The test for converting a stacked DataArray to a DataFrame or Series failed.") from e

if __name__ == "__main__":
    main()
