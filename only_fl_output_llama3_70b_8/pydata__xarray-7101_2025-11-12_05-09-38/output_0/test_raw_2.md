Here is the standalone Python file `reproducer.py` to reproduce the issue:
```python
import xarray as xr
import traceback
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    ds = xr.DataArray(
        [[[1, 1], [0, 0]], [[2, 2], [1, 1]]],
        dims=("lat", "year", "month"),
        coords={"lat": [-60, 60], "year": [2010, 2020], "month": [3, 6]},
        name="test",
    ).to_dataset()

    stacked = ds.stack(time=("year", "month"))
    stacked = stacked.assign_coords(
        {"time": [y + m / 12 for y, m in stacked["time"].values]}
    )

    assert set(stacked._variables.keys()) == {"test", "time", "lat"}
    assert set(stacked._coord_names) == {"time", "lat"}

except Exception as e:
    print_stacktrace(e)
    if isinstance(e, AssertionError):
        raise
    else:
        raise AssertionError("Issue is not present")
```
This script will reproduce the issue and raise an `AssertionError` when the issue is present, printing a stack trace of the issue. If the issue is fixed, the script will exit with code 0.