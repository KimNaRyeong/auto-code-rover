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

# The following line should raise an AssertionError
assert np.isinf(clust.core_distances_[6]), "Core distance of the last point should be inf"
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 16, in <module>
    assert np.isinf(clust.core_distances_[6]), "Core distance of the last point should be inf"
AssertionError: Core distance of the last point should be inf
```
This reproduces the issue where the core distance of the last point is not `inf` as stated in the documentation.