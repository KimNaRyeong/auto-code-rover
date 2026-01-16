Sure, below is a Python script `reproducer.py` that aims to reproduce the issue laid out. The script tests the performance of `randomized_svd` with different sparse matrix types and raises `AssertionError` if any matrix type takes significantly more time than the csr_matrix, which is used as a baseline for comparison. 

This script follows best practices by encapsulating test logic in a function, utilizing a simple performance timing approach, and making use of your specific stack trace printing function for clear error reporting. Note that the threshold for "significantly more time" is somewhat arbitrary and may need adjustment based on your expectations and the variability of execution times across different systems.

```python
import numpy as np
import scipy.sparse as sp
from sklearn.utils.extmath import randomized_svd
import time

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

def test_performance(X, n_iter=50):
    start_time = time.time()
    for _ in range(n_iter):
        U, S, VT = randomized_svd(X, 50, random_state=42)
    end_time = time.time()
    return (end_time - start_time) / n_iter

def main():
    np.random.seed(42)
    data = np.random.normal(0, 1, [1000, 1000]) * np.random.poisson(0.1, [1000, 1000])
    formats = ['csr', 'csc', 'bsr', 'coo', 'lil', 'dok']
    
    baseline_time = 0
    acceptable_slowdown = 5  # Chosen factor of acceptable slowdown, may require adjustment

    try:
        for format in formats:
            X = getattr(sp, f"{format}_matrix")(data)
            avg_time = test_performance(X)
            print(f"Average time for {format}_matrix: {avg_time:.3f} seconds")
            if format == 'csr':
                baseline_time = avg_time
            else:
                assert avg_time <= baseline_time * acceptable_slowdown, f"{format}_matrix is significantly slower than expected!"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
```

Important considerations:

- This script takes a simplistic approach by measuring average time across several iterations (defined by `n_iter`). Real-world scenarios might require more sophisticated statistical methods to account for variability.
- The `acceptable_slowdown` factor is arbitrary and should be calibrated based on your performance expectations and the variability of measurements across different runs and systems.
- The script exits normally (with a code of 0) when all tests pass, including the case when an issue is fixed. If an `AssertionError` is encountered, it will print the stack trace detailing which assertion failed, fulfilling the requirement of clear error reporting.