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
    import xarray as xr

    da = xr.DataArray([0, 0], dims="x", attrs={'units': 'K'})
    out = da.quantile(.9, dim='x', keep_attrs=True)
    
    try:
        assert out.attrs == {'units': 'K'}, "Attributes not preserved"
    except AssertionError as e:
        print_stacktrace(e)
        raise

    print("Test passed. `keep_attrs` is working as expected.")

if __name__ == "__main__":
    main()
```

This script checks if the `quantile` method in the xarray library correctly retains attributes when `keep_attrs=True` is used. If the issue is present, it will raise an `AssertionError` and print a detailed stack trace, pinpointing where the failure occurred. When the issue is fixed, it exits with code 0, indicating success.