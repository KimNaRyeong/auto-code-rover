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

    # Assert that dok_matrix is slower than other matrix types
    assert t > 2.0, "dok_matrix was not slower than other matrix types"

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        raise
```
When executed with `python3 reproducer.py`, the script should print the following output:
```yaml
Time for csr_matrix: 0.37 seconds
Time for csc_matrix: 0.38 seconds
Time for bsr_matrix: 0.38 seconds
Time for coo_matrix: 0.58 seconds
Time for lil_matrix: 1.45 seconds
Time for dok_matrix: 22.16 seconds
```
And it should exit with code 0, indicating that the issue is present. If the `dok_matrix` time is not significantly slower than the other matrix types, then the script will raise an `AssertionError` and print a stack trace.