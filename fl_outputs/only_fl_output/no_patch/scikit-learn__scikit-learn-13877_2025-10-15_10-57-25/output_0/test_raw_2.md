Below is a revised version of the `reproducer.py` script based on your requirements. This script is designed to reproduce the described issue with the `pairwise_distances` function from scikit-learn, specifically the problem where using the function with the cosine metric and parallel execution (`n_jobs` parameter) results in incorrect zero values, and the issue with euclidean distances being returned as integers instead of floats under certain conditions. This script incorporates error handling and conditional checks to assert the correctness of the operation and outputs an appropriate stack trace on failure.

```python
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

def main():
    X = np.array([
        [1, 3],
        [2, 1],
        [3, 2]
    ])

    # Test for cosine metric
    try:
        distances_cosine = pairwise_distances(X, metric='cosine', n_jobs=-1)
        assert not np.allclose(distances_cosine, np.zeros_like(distances_cosine)), "Cosine distances are incorrectly all zeros."
        print("Cosine metric test passed.")
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

    # Test for euclidean metric, checking type consistency on n_jobs parameter change
    try:
        distances_euclidean = pairwise_distances(X, metric='euclidean', n_jobs=-1)
        assert distances_euclidean.dtype == float, "Euclidean distances are not float type."
        print("Euclidean metric test passed.")
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```
This script specifically tests for the issues described in your report:

1. It first runs the `pairwise_distances` function with the `cosine` metric under parallel execution conditions (`n_jobs=-1`) and asserts that the result should not be all zeros. If the assertion fails (meaning the issue is present), it captures and prints the stack trace.

2. It then runs the function with the `euclidean` metric under the same conditions and asserts that the results' data type is float, addressing the second part of the issue where results were returned as integers instead of floats when they shouldn't be. 

Remember to replace `"cosine"` with any other metrics and adjust `n_jobs` parameters as necessary to test different configurations or other aspects of the function. This script exits with code 1 upon failure, indicating that the issue(s) are present.