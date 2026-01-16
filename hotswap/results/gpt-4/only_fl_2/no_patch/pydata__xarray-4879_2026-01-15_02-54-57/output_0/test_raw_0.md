```python
# reproducer.py
import xarray as xr
import numpy as np
from pathlib import Path

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

def test_repr(path, nx):
    ds = xr.DataArray(np.random.rand(nx))
    if path.exists():
        path.unlink()
    ds.to_netcdf(path)

def main():
    path = Path("saved_on_disk.nc")
    try:
        # First test run
        test_repr(path, 4)
        first_run_data = xr.open_dataset(path)
        first_run_data.load()  # Load data to ensure it's read from disk now
        
        # Second test run
        test_repr(path, 5)
        second_run_data = xr.open_dataset(path)
        second_run_data.load()  # Load data to ensure it's read from disk now

        # Compare shapes to see if data has been correctly reloaded
        assert first_run_data.shape != second_run_data.shape, "Data shape did not change between runs."
        
        # Further assertions can be added as required.
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    except Exception as e:
        print_stacktrace(e)
        exit(1)
    finally:
        if path.exists():
            path.unlink()

if __name__ == "__main__":
    main()
```