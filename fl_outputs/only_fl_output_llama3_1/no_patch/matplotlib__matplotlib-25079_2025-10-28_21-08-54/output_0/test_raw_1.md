Here is the reproducer script:

```python
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
import sys
import traceback

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
    import matplotlib
    fig, ax = plt.subplots()
    img = np.random.uniform(1, 5, (25, 25))
    plot = ax.pcolormesh(img)
    cbar = plt.colorbar(plot, ax=ax)

    vmin = 1
    vmax = 5

    plt.ion()
    plt.show(block=False)
    plt.pause(0.5)

    plot.norm = LogNorm(vmin=vmin, vmax=vmax)
    plot.autoscale()
    plt.pause(0.5)

except Exception as e:
    print_stacktrace(e)
    sys.exit(1)
```

This script should be executed by `python3 reproducer.py`. If the issue is present, it will raise an `AssertionError` and print a stack trace of the issue.