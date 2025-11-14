Here is the reproducer script:
```python
import xarray as xr
from pathlib import Path
import numpy as np
import os

def test_repr(nx):
    ds = xr.DataArray(np.random.rand(nx))
    path = Path("saved_on_disk.nc")
    if path.exists():
        path.unlink()
    ds.to_netcdf(path)
    return path

def main():
    try:
        os.remove("saved_on_disk.nc")  # Clean up any previous files
    except FileNotFoundError:
        pass

    for nx in [4, 5]:
        test_repr(nx)

    with open("saved_on_disk.nc", "rb") as f:
        data = f.read()

    assert len(data) > 0, "File not found or empty"

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        raise
    else:
        print("Issue reproduced successfully")
        exit(0)

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

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        raise
    else:
        print("Issue reproduced successfully")
        exit(0)

print_stacktrace(AssertionError("File not found or empty"))
```
This script will run the `test_repr` function twice, once for each value of `nx`, and then attempt to read the resulting NetCDF file using a binary open. If the issue is present, an assertion error should be raised. The script will then print the stack trace of the error.

To run the reproducer, save this code in a file named `reproducer.py` and execute it with Python 3: `python3 reproducer.py`.