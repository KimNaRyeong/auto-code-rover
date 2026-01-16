```python
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
    import sys
    import numpy as np
    from sklearn.cluster import OPTICS

    X = np.array([-5, -2, -4.8, -1.8, -5.2, -2.2, 100, 200, 4, 2, 3.8, 1.8, 4.2, 2.2])
    X = X.reshape(-1, 2)
    clust = OPTICS(min_samples=3, max_bound=1)
    clust.fit(X)
    core_distances = clust.core_distances_

    expected = np.array([0.28284271, 0.56568542, 0.56568542, np.inf,
                         0.28284271, 0.56568542, 0.56568542])

    try:
        assert np.allclose(core_distances[core_distances != np.inf], expected[expected != np.inf], equal_nan=True), "core distances do not match expected values"
        assert np.any(np.isinf(core_distances)) == np.any(np.isinf(expected)), "Inconsistent handling of infinitely distant points"
        print("Issue not present, OPTICS core distances are consistent.")
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
        sys.exit(0)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```