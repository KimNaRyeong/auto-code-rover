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
    from pylab import *
    tripcolor(np.random.rand(100), np.random.rand(100), np.random.rand(100), clim=(0, 0.5))
    colorbar()
    show()

    # Check if the color limits are respected
    clim = plt.gca().images[0].get_clim()
    assert clim == (0, 0.5), "tripcolor ignores clim"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
```
This script will raise an `AssertionError` if the issue is present and print a stack trace of the issue. If the issue is fixed, it will exit with code 0.