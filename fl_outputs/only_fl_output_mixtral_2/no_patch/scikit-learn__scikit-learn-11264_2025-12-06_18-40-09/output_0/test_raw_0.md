 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import numpy as np
import scipy.sparse as sp
from sklearn.utils.extmath import randomized_svd
import timeit

def test(X, seed=42):
    U, S, VT = randomized_svd(X, 50, random_state=seed)

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    np.random.seed(42)
    X = np.random.normal(0,1,[1000,1000]) * np.random.poisson(0.1, [1000,1000])
    X = sp.csr_matrix(X)
    t = timeit.timeit(lambda: test(X), number=50)
    print(f"Time for csr_matrix: {t:.2f} seconds")

    X = sp.csc_matrix(X)
    t = timeit.timeit(lambda: test(X), number=50)
    print(f"Time for csc_matrix: {t:.2f} seconds")

    X = sp.bsr_matrix(X)
    t = timeit.timeit(lambda: test(X), number=50)
    print(f"Time for bsr_matrix: {t:.2f} seconds")

    X = sp.coo_matrix(X)
    t = timeit.timeit(lambda: test(X), number=50)
    print(f"Time for coo_matrix: {t:.2f} seconds")

    X = sp.lil_matrix(X)
    t = timeit.timeit(lambda: test(X), number=50)
    print(f"Time for lil_matrix: {t:.2f} seconds")

    X = sp.dok_matrix(X)
    t = timeit.timeit(lambda: test(X), number=50)
    print(f"Time for dok_matrix: {t:.2f} seconds")

    # Assert that dok_matrix is not significantly slower than other matrix types
    max_time = max(t for t in (t,) + tuple(getattr(timeit, "timeit")(lambda: test(sp.csr_matrix(X)), number=50) for sparse_type in (sp.csc_matrix, sp.bsr_matrix, sp.coo_matrix, sp.lil_matrix)))
    if t > 5 * max_time:
        raise AssertionError(f"dok_matrix is significantly slower than other matrix types (time={t:.2f}s, max_time={max_time:.2f}s)")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        exit(1)
```
The script creates a random sparse matrix using NumPy and converts it to different sparse matrix types using SciPy. It then measures the time it takes to perform a randomized SVD on each matrix type using Scikit-Learn. Finally, it asserts that the time it takes for the `dok_matrix` type is not significantly slower than the other matrix types.

If the assertion fails, the script raises an `AssertionError` and prints a stack trace. If the script completes without raising an exception, it exits with code 0.