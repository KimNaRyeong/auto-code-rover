```python
import xarray as xr
import numpy as np

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

def test_center_justified_rolling():
    my_data = xr.DataArray(np.arange(1,10), dims="x")

    # Option 1: take a center-justified rolling average
    result1 = my_data.rolling(x=3, center=True).mean().values
    
    # Option 2: try to manually iterate, but expecting center-justified results
    my_data_rolling = my_data.rolling(x=3, center=True)
    result2 = np.array([window.mean().values.item() for label, window in my_data_rolling])
    
    try:
        # Assert that both methods produce the same results
        assert np.array_equal(result1, result2), "Mismatch in results between automatic and manual center-justified rolling operation."
    except AssertionError as e:
        print_stacktrace(e)
        raise e

if __name__ == "__main__":
    test_center_justified_rolling()
```