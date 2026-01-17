 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from sklearn.cluster import OPTICS
import numpy as np

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

X = np.array([-5, -2, -4.8, -1.8, -5.2, -2.2, 100, 200, 4, 2, 3.8, 1.8, 4.2, 2.2])
X = X.reshape(-1, 2)
clust = OPTICS(min_samples=3, max_bound=1)
clust.fit(X)

# Assert that there is a point with a core distance of inf
assert np.isinf(clust.core_distances_).any(), "Core distances do not contain inf"

print("Core distances:")
print(clust.core_distances_)
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` with a stack trace, indicating that the issue is present.

The script creates a 2D array `X` with some arbitrary values, creates an `OPTICS` object with `min_samples=3` and `max_bound=1`, fits the object to the data, and then checks if there is a point with a core distance of `inf`. If there is no point with a core distance of `inf`, the script raises an `AssertionError` with a message. The script then prints the core distances.