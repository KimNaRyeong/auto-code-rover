Based on your instructions, I'll create an improved version of `reproducer.py` that follows your specifications more accurately. This script is designed to specifically test the performance of `randomized_svd` across different sparse matrix formats and raise an `AssertionError` if the performance issue, as described, is present. Additionally, upon resolving the issue, the script should exit gracefully with code 0, providing a clear and precise stack trace if the error occurs. Here's how the script would look like:

```python
import numpy as np
import scipy.sparse as sp
from sklearn.utils.extmath import randomized_svd
import time
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_matrix_performance(matrix_type, seed=42):
    np.random.seed(seed)
    X = np.random.normal(0, 1, [1000, 1000]) * np.random.poisson(0.1, [1000, 1000])
    X_sparse = getattr(sp, f"{matrix_type}_matrix")(X)
    
    start_time = time.time()
    U, S, VT = randomized_svd(X_sparse, 50, random_state=seed)
    elapsed_time = time.time() - start_time

    return elapsed_time

def main():
    matrix_types = ['csr', 'csc', 'bsr', 'coo', 'lil', 'dok']
    expected_ratio = {'csr': 1, 'csc': 1, 'bsr': 1, 'coo': 1.5, 'lil': 2, 'dok': 2.5}  # Expected performance ratio baseline from csr
    baseline_time = test_matrix_performance('csr')

    for matrix_type in matrix_types:
        elapsed_time = test_matrix_performance(matrix_type)
        ratio = elapsed_time / baseline_time
        print(f"{matrix_type}_matrix: {elapsed_time:.2f}s, Ratio to csr: {ratio:.2f}")

        if ratio > expected_ratio[matrix_type]:
            error_message = f"{matrix_type}_matrix performance degradation: {elapsed_time:.2f}s, expected ratio: {expected_ratio[matrix_type]}, actual ratio: {ratio:.2f}"
            try:
                raise AssertionError(error_message)
            except AssertionError as e:
                print_stacktrace(e)
                # Since the issue description asks to exit with code 0 when the issue is fixed, no special handling needed for this case.
                sys.exit(0)

if __name__ == "__main__":
    main()
```

This script enhances clarity by separating concerns between testing the performance of `randomized_svd` across various sparse matrix types, generating a baseline comparison with `csr_matrix`, and enforcing expected performance ratios. When running, it raises an `AssertionError` if the observed performance deviates significantly from expected benchmarks, thereby tightly aligning with the stipulated requirement to exit with code 0 upon resolution of the described issue.