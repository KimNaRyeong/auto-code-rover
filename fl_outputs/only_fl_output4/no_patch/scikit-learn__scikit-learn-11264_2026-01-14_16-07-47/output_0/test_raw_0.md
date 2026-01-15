```python
# reproducer.py
import numpy as np
import scipy.sparse as sp
from sklearn.utils.extmath import randomized_svd
import timeit

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

def test(X, seed=42):
    U, S, VT = randomized_svd(X, 50, random_state=seed)

def measure_time(matrix_constructor):
    np.random.seed(42)
    X = np.random.normal(0, 1, [1000, 1000]) * np.random.poisson(0.1, [1000, 1000])
    X = matrix_constructor(X)
    return timeit.timeit(lambda: test(X), number=5)

def main():
    csr_time = measure_time(sp.csr_matrix)
    csc_time = measure_time(sp.csc_matrix)
    bsr_time = measure_time(sp.bsr_matrix)
    coo_time = measure_time(sp.coo_matrix)
    lil_time = measure_time(sp.lil_matrix)
    dok_time = measure_time(sp.dok_matrix)

    # Check for significant performance discrepancies
    try:
        assert dok_time < 5 * lil_time, "DOK matrix processing is significantly slower than expected."
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    except Exception as e:
        print_stacktrace(e)
        exit(1)
    
    print("Issue not present or has been fixed. Exiting with code 0.")
    exit(0)

if __name__ == '__main__':
    main()
```

This script first tests the performance of `randomized_svd` with various sparse matrix formats and measures the execution time for each. It specifically checks if the `dok_matrix` processing time is disproportionately larger than that of the `lil_matrix`. An `AssertionError` is raised if the `dok_matrix` processing time exceeds the `lil_matrix` time by a significant factor, indicating the presence of the issue. If the performance discrepancy isn't observed, it suggests that the issue is either not present or has been fixed, and the script exits with code 0.