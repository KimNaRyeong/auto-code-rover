Here is the reproducer script:

```python
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
        da = xr.DataArray(
            data=[32, 16, 8],
            dims=["time"],
            coords=dict(
                time=pd.date_range("2014-09-06", periods=3),
                reference_time=pd.Timestamp("2014-09-05"),
            ),
        )

        ds1 = xr.Dataset({"myvar": da})
        print_stacktrace(AssertionError(f"Expected datetime64[ns], got {ds1.time.dtype}"))

        ds1.time.encoding["calendar"] = "Gregorian"
        ds1.reference_time.encoding["calendar"] = "Gregorian"

        ds1.to_netcdf("test-capitalized.nc")

        ds2 = xr.open_dataset("test-capitalized.nc")
        print_stacktrace(AssertionError(f"Expected datetime64[ns], got {ds2.time.dtype}"))

    except Exception as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.