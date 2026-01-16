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

def main():
    import numpy as np
    from sklearn.cluster import OPTICS

    X = np.array([-5, -2, -4.8, -1.8, -5.2, -2.2, 100, 200, 4, 2, 3.8, 1.8, 4.2, 2.2])
    X = X.reshape(-1, 2)
    clust = OPTICS(min_samples=3, max_bound=1)
    clust.fit(X)
    core_distances = clust.core_distances_

    # Expect points that will never be core to have a core distance of infinity
    expected = [np.inf if np.isinf(x) else 0.28284271 for x in core_distances]
    
    try:
        np.testing.assert_allclose(core_distances, expected, rtol=1e-05, atol=1e-08)
        print("Test passed: Core distances are as expected.")
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        main()
    except AssertionError:
        exit(1)  # Exit with a non-zero code if the issue is present
    else:
        exit(0)  # Exit with 0 when the issue is fixed or not present
```