Here is the reproducer script:

```python
import matplotlib.pyplot as plt
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

def reproduce_issue():
    try:
        x = np.linspace(0, 2 * np.pi, 100)
        y = np.sin(x)
        poly = plt.Polygon([[1, 1], [1, 0], [0, 0], [0, 1]], closed=True)
        plt.contourf(np.cos(x) + np.random.normal(size=len(x)), np.sin(x) + np.random.normal(size=len(x)), y, clip_path=poly)
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    reproduce_issue()
```

This script will attempt to create a contour plot with a polygonal clip path. If the issue is present (i.e., the `clip_path` argument is ignored), it will print the stack trace and raise an `AssertionError`.