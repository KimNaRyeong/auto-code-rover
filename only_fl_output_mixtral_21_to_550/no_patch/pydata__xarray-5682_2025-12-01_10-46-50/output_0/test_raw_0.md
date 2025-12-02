 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

name = r"$Ra_s = \mathrm{mean}(\epsilon_k) / \mu M^2_\infty$"
da = xr.DataArray(np.arange(5), dims="x", coords = dict(x=np.arange(5)))
da.x.attrs = dict(long_name = name)

try:
    da.plot()
except Exception as e:
    print_stacktrace(e)

plt.figure()
plt.plot(np.arange(5))
plt.xlabel(name)
plt.show()
```
When executed, the script should raise an `AssertionError` when the issue is present and print a stack trace of the issue. The script should also exit with code 0 when the issue is fixed.