To address the specific requirements for reproducing the issue with `pairwise_distances` returning zeros for the `cosine` metric when executed in parallel, and handling of expected outputs, here is a standalone Python script. This script is designed to be placed in the root directory of a project and executed with Python 3. It includes comprehensive error handling and reporting through the provided `print_stacktrace` function to help debug the scenario effectively.

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

    # Expected Results for cosine
    expected_cosine = np.array([
        [0., 0.29289322, 0.21064778],
        [0.29289322, 0., 0.00772212],
        [0.21064778, 0.00772212, 0.]
    ])

    # Expected Results for euclidean
    expected_euclidean = np.array([
        [0., 2.23606798, 2.23606798],
        [2.23606798, 0., 1.41421356],
        [2.23606798, 1.41421356, 0.]
    ])

    try:
        for metric in ['cosine', 'euclidean']:
            for n_jobs in [-1, 1, 2]:
                results = pairwise_distances(X, metric=metric, n_jobs=n_jobs)
                if metric == 'cosine':
                    assert np.allclose(results, expected_cosine), f"Failed for metric={metric} with n_jobs={n_jobs}"
                else:
                    assert np.allclose(results, expected_euclidean), f"Failed for metric={metric} with n_jobs={n_jobs}"
        print("Success: All tests passed. The issue is fixed or could not be reproduced.")
    except AssertionError as ae:
        print_stacktrace(ae)
        exit(1)
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    check_pairwise_distances()
```

This script checks the results of `pairwise_distances` against expected outcomes for both `cosine` and `euclidean` metrics across different `n_jobs` settings. It raises an `AssertionError` when results do not meet expectations, facilitating the identification of conditions under which the issue occurs. If the issue has been resolved, it will exit with code 0, indicating success.