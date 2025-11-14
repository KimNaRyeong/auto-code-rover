Here is the reproducer script:

```python
import numpy as np
from sklearn.cluster import OPTICS

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
    X = np.array([-5, -2, -4.8, -1.8, -5.2, -2.2, 100, 200, 4, 2, 3.8, 1.8, 4.2, 2.2])
    X = X.reshape(-1, 2)
    clust = OPTICS(min_samples=3, max_eps=1)
    try:
        clust.fit(X)
        core_distances = clust.core_distances_
        if not np.isinf(core_distances[6]):
            raise AssertionError("Expected Inf in the 7th position of core_distances_")
    except Exception as e:
        print_stacktrace(e)

if __name__ == "__main__":
    reproduce_issue()
```

You can run this script by executing `python3 reproducer.py` in your terminal. If the issue is present, it will raise an AssertionError and print a stack trace.