 I apologize for the mistake in the previous response. Here is the corrected standalone python file `reproducer.py` to reproduce the issue:

```python
import xarray as xr
import numpy as np

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == "__main__":
    da = xr.DataArray(np.arange(24), dims=["time"])
    da = da.assign_coords(day=365 * da)
    ds = da.to_dataset(name="T")

    expected_ds = ds.copy()

    try:
        result_ds = ds.coarsen(time=12).construct(time=("year", "month"))
        assert "day" not in result_ds.data_vars
    except AssertionError as e:
        print_stacktrace(e)
        exit(0)
    except Exception as e:
        print_stacktrace(e)
        exit(1)
```

When executed with `python3 reproducer.py`, the script should exit with code 0 because the `day` coordinate is demoted to a variable in the `result_ds` dataset. This demonstrates the issue in xarray. The line numbers of the statements should be shown clearly in the stack trace.