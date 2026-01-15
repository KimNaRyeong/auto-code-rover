```python
# reproducer.py

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


def check_core_distances():
    # Dataset creation
    X = np.array([-5, -2, -4.8, -1.8, -5.2, -2.2, 100, 200, 4, 2, 3.8, 1.8, 4.2, 2.2])
    X = X.reshape(-1, 2)
    # OPTICS clustering
    clust = OPTICS(min_samples=3, max_bound=1)
    clust.fit(X)
    core_distances = clust.core_distances_
    
    # Assertion: Points which will never be core have a distance of inf
    try:
        assert np.isinf(core_distances[-1]), "Points which will never be core must have a distance of inf."
    except AssertionError as e:
        print_stacktrace(e)
        raise e
    
    print("No issue found.")

if __name__ == "__main__":
    try:
        check_core_distances()
    except AssertionError:
        pass
    else:
        # Exit with code 0 if the issue is fixed.
        exit(0)
```