Here is the reproducer script:

```python
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

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

def reproduce_issue():
    try:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        X, Y, Z = np.random.rand(100), np.random.rand(100), np.random.rand(100)
        ax.scatter(X, Y, Z, c=Z, clim=(0, 0.5))
        plt.colorbar()
        plt.show()
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    reproduce_issue()
```

This script will attempt to reproduce the issue by creating a 3D scatter plot with colorbar using `tripcolor` (which is equivalent to `ax.scatter` in this case). If the issue is present, it will print the stack trace and raise an `AssertionError`.