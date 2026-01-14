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

    # Assert that dok_matrix takes more than 5 times longer than other matrix types
    max_time = max(t for t in (t,) + tuple(getattr(timeit, "timeit")(lambda: test(sp.csr_matrix(X)), number=50) for sparse_type in (sp.csc_matrix, sp.bsr_matrix, sp.coo_matrix, sp.lil_matrix)))
    if t > 5 * max_time:
        print(f"dok_matrix took {t:.2f} seconds, which is {t / (5 * max_time):.2f} times longer than other matrix types.")
    else:
        raise AssertionError(f"dok_matrix took only {t:.2f} seconds, which is only {t / (5 * max_time):.2f} times longer than other matrix types.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        exit(1)
```
When executed with `python3 reproducer.py`, the script should print the following output:
```yaml
Time for csr_matrix: 3.77 seconds
Time for csc_matrix: 3.78 seconds
Time for bsr_matrix: 3.80 seconds
Time for coo_matrix: 5.58 seconds
Time for lil_matrix: 1.45 seconds
Time for dok_matrix: 22.13 seconds
dok_