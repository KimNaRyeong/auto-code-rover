Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import numpy as np
import matplotlib.pyplot as plt

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

try:
    np.random.seed(0)  # for reproducibility
    x, y, c = np.random.rand(100), np.random.rand(100), np.random.rand(100)
    plt.tripcolor(x, y, c, clim=(0, 0.5))
    cb = plt.colorbar()
    vmin, vmax = cb.get_clim()
    assert vmin == 0 and vmax == 0.5, "tripcolor ignores clim"
    print("Issue is fixed!")
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

plt.show()
```
This script will raise an `AssertionError` if the issue is present, printing a stack trace of the error. If the issue is fixed, it will print "Issue is fixed!" and exit with code 0.