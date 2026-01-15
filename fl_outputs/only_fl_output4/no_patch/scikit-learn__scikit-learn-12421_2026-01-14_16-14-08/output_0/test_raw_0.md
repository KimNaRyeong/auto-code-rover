```python
# reproducer.py

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


def test_optics_core_distances():
    import numpy as np
    from sklearn.cluster import OPTICS

    # Prepare the dataset
    X = np.array([-5, -2, -4.8, -1.8, -5.2, -2.2, 100, 200, 4, 2, 3.8, 1.8, 4.2, 2.2])
    X = X.reshape(-1, 2)

    # Perform clustering
    clust = OPTICS(min_samples=3, max_bound=1)
    clust.fit(X)

    # Check if any distance is 'inf' as expected
    if not np.isinf(clust.core_distances_).any():
        raise AssertionError("OPTICS: self.core_distances_ does not contain 'inf' for points that will never be core as expected.")

try:
    test_optics_core_distances()
except AssertionError as e:
    print_stacktrace(e)
    raise SystemExit(1)
else:
    print("No issue detected.")
    raise SystemExit(0)
```