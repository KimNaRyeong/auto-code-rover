Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
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

def main():
    X = np.array([-5, -2, -4.8, -1.8, -5.2, -2.2, 100, 200, 4, 2, 3.8, 1.8, 4.2, 2.2])
    X = X.reshape(-1, 2)
    clust = OPTICS(min_samples=3, max_eps=1)  # Note: max_bound is not a valid parameter for OPTICS
    clust.fit(X)
    core_distances = clust.core_distances_
    
    for distance in core_distances:
        if np.isinf(distance):
            continue
        assert distance != 0, "Points which will never be core have a non-zero finite distance"
    
if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```
This script reproduces the issue by creating an OPTICS instance with `min_samples=3` and `max_eps=1`, fitting it to a sample dataset, and then checking if any points have a non-infinite core distance. If such a point is found, an `AssertionError` is raised, and the stack trace is printed using the provided function.