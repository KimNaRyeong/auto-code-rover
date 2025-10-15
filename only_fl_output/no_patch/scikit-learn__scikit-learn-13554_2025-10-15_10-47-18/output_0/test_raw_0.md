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

def test_euclidean_distances_precision():
    import numpy as np
    import sklearn.metrics.pairwise

    a_64 = np.array([61.221637725830078125, 71.60662841796875, -65.7512664794921875], dtype=np.float64)
    b_64 = np.array([61.221637725830078125, 71.60894012451171875, -65.72847747802734375], dtype=np.float64)

    a_32 = a_64.astype(np.float32)
    b_32 = b_64.astype(np.float32)

    dist_64_np = np.array([np.linalg.norm(a_64 - b_64)], dtype=np.float64)
    dist_32_np = np.array([np.linalg.norm(a_32 - b_32)], dtype=np.float32)

    dist_64_sklearn = sklearn.metrics.pairwise.pairwise_distances([a_64], [b_64])
    dist_32_sklearn = sklearn.metrics.pairwise.pairwise_distances([a_32], [b_32])

    try:
        assert np.allclose(dist_64_np, dist_64_sklearn, rtol=1e-9), "64-bit computation mismatch"
        assert np.allclose(dist_32_np, dist_32_sklearn, rtol=1e-9), "32-bit computation mismatch"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        test_euclidean_distances_precision()
    except AssertionError:
        exit(1)
    print("All tests passed successfully!")
    exit(0)
```