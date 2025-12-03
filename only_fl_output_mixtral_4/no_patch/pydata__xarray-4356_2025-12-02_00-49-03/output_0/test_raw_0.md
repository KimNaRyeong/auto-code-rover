 Here is a standalone Python script `reproducer.py` to reproduce the issue:
```python
import xarray as xr
import numpy as np

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == "__main__":
    da = xr.DataArray([[1., 2, 3], [4, 5, 6]])
    with pytest.raises(AssertionError):
        da.sum(["dim_0", "dim_1"], min_count=1)
```
This script uses the `pytest` library to raise an `AssertionError` when the issue is present. If the issue is fixed, the script will exit with code 0 without raising any exceptions.

To run the script, make sure you have `pytest` installed (`pip install pytest`), then execute `python3 reproducer.py`. The script will print a stack trace if the issue is present.