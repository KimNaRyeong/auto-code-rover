Certainly! Here is a refined approach to construct a `reproducer.py` script to specifically address and reproduce the issue mentioned:

```python
# reproducer.py
import numpy as np
from sklearn.metrics import pairwise_distances

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

def check_pairwise_distances():
    X = np.array([
        [1, 3],
        [2, 1],
        [3, 2]
    ])

    # Check for cosine metric with n_jobs=-1
    try:
        results_cosine_parallel = pairwise_distances(X, metric='cosine', n_jobs=-1)
        assert not np.all((results_cosine_parallel == 0)), "Cosine metric with n_jobs=-1 returns zeros"
    except AssertionError as e:
        print("Cosine metric with n_jobs=-1 FAILED:")
        print_stacktrace(e)

    # Check for cosine metric with n_jobs=1
    try:
        results_cosine_single = pairwise_distances(X, metric='cosine', n_jobs=1)
        expected_cosine = np.array([
            [0., 0.29289322, 0.21064778],
            [0.29289322, 0., 0.00772212],
            [0.21064778, 0.00772212, 0.]
        ])
        assert np.allclose(results_cosine_single, expected_cosine, atol=1e-7), "Cosine metric with n_jobs=1 returns incorrect values"
    except AssertionError as e:
        print("Cosine metric with n_jobs=1 FAILED:")
        print_stacktrace(e)

    # Check euclidean metric behaves consistently across n_jobs settings
    try:
        results_euclidean_parallel = pairwise_distances(X, metric='euclidean', n_jobs=-1)
        results_euclidean_single = pairwise_distances(X, metric='euclidean', n_jobs=1)
        assert np.all(results_euclidean_parallel == results_euclidean_single.astype(int)), "Euclidean metric returns inconsistent types across n_jobs settings"
    except AssertionError as e:
        print("Euclidean metric behavior inconsistent across n_jobs settings:")
        print_stacktrace(e)

def main():
    check_pairwise_distances()
    print("If no exceptions were raised, the tests have passed.")

if __name__ == "__main__":
    main()
```

This script does the following:
- It defines the expected behavior for the `cosine` and `euclidean` metrics under various `n_jobs` settings and tests against these expectations.
- For the `cosine` metric tests, it ensures that results are not all zeros when `n_jobs=-1` and matches the precomputed expected values for `n_jobs=1`.
- For the `euclidean` metric, it checks if the behavior remains consistent across different `n_jobs` settings.
- If the assertions fail, it prints a stacktrace to help identify where and why the failure occurred.

This structure helps in isolating each tested condition and provides clear feedback on which aspect of the functionality is not behaving as expected.