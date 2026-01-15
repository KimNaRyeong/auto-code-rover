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


def test_optics_core_distances_issue():
    import numpy as np
    from sklearn.cluster import OPTICS

    X = np.array([-5, -2, -4.8, -1.8, -5.2, -2.2, 100, 200, 4, 2, 3.8, 1.8, 4.2, 2.2])
    X = X.reshape(-1, 2)
    clust = OPTICS(min_samples=3, max_bound=1)
    clust.fit(X)
    
    # Assert that an inf value is expected in core_distances_ for points that will never be core
    try:
        assert np.isinf(clust.core_distances_).any(), "No 'inf' value found in core_distances_ for points that will never be core"
        print("Test passed: 'inf' value found in core_distances_ as expected.")
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)

if __name__ == "__main__":
    try:
        test_optics_core_distances_issue()
    except Exception as e:
        print_stacktrace(e)
        raise SystemExit(1)
    else:
        raise SystemExit(0)
```

This script attempts to verify if the `core_distances_` attribute of the `OPTICS` object contains infinity values for points that will never be core points, consistent with the expected behavior as documented. If the check fails (meaning that it does not find any `inf` values where they are expected), it will raise an `AssertionError` and exit with code 1, indicating the presence of the issue. Conversely, if the script does not raise an error, it exits with code 0, implying that the issue is resolved or not present.