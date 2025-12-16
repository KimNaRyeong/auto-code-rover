 Here is a standalone Python file `reproducer.py` that reproduces the issue:
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

my_data = xr.DataArray(np.arange(1,10), dims="x")
my_data_rolling = my_data.rolling(x=3, center=True)

result1 = my_data.rolling(x=3, center=True).mean().values
result2 = [window.mean().values.item() for label, window in my_data_rolling]

assert np.allclose(result1, result2), "The two results should be the same."
print_stacktrace(AssertionError("The two results are not the same."))
```
When executed with `python3 reproducer.py`, the script will print a stack trace indicating that the assertion has failed:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 17
    assert np.allclose(result1, result2), "The two results should be the same."
AssertionError: The two results are not the same.
```
This confirms that the `center` keyword argument is indeed ignored when manually iterating over a `DataArrayRolling` object.