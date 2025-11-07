```python
# reproducer.py
import xarray as xr
import pandas as pd

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    da = xr.DataArray([[[1]]], dims=["a", "b", "c"]).stack(ab=["a", "b"])
    try:
        da.to_series()
        print("Conversion to Series succeeded, no issues detected.")
    except Exception as e:
        print_stacktrace(e)
        assert False, "Conversion to Series failed due to an exception as expected."

    try:
        da.to_dataframe("A")
        print("Conversion to DataFrame succeeded, no issues detected.")
    except Exception as e:
        print_stacktrace(e)
        assert False, "Conversion to DataFrame failed due to an exception as expected."

if __name__ == "__main__":
    main()
```