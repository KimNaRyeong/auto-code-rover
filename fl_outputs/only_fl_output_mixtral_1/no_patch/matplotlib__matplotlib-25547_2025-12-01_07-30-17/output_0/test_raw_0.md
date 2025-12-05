 Here is a standalone python script `reproducer.py` to reproduce the issue:
```python
import matplotlib.pyplot as plt
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

try:
    fig, ax = plt.subplots(1, 1)
    ax.errorbar([0], [0], [np.nan])
except Exception as e:
    print_stacktrace(e)
    assert False

plt.show()
```
When executed, the script should raise a `UserWarning` about converting masked values to null. This is because the `errorbar` function calls `_upcast_err` which looks for a first finite element in `yerr`. When `yerr` contains only `NaN` values, it raises a `StopIteration` error.

To fix the issue, the `_upcast_err` function should handle the case when `yerr` contains only `NaN` values. One possible solution is to check if `yerr` is an array of `NaN` values and return an empty array in this case. This will prevent the `StopIteration` error and the function will work as expected.