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

def test():
    import numpy as np
    import scipy.sparse as sp
    from sklearn.utils.extmath import randomized_svd
    import time

    def time_svd(X):
        start_time = time.time()
        U, S, VT = randomized_svd(X, 50, random_state=42)
        return time.time() - start_time

    np.random.seed(42)
    X_dense = np.random.normal(0, 1, [1000, 1000]) * np.random.poisson(0.1, [1000, 1000])
    X_csr = sp.csr_matrix(X_dense)
    X_csc = sp.csc_matrix(X_dense)
    X_bsr = sp.bsr_matrix(X_dense)
    X_coo = sp.coo_matrix(X_dense)
    X_lil = sp.lil_matrix(X_dense)
    X_dok = sp.dok_matrix(X_dense)

    csr_time = time_svd(X_csr)
    csc_time = time_svd(X_csc)
    bsr_time = time_svd(X_bsr)
    coo_time = time_svd(X_coo)
    lil_time = time_svd(X_lil)
    dok_time = time_svd(X_dok)

    max_expected_time = csr_time * 5  # Let's say we allow up to 5 times slower than CSR as tolerable

    try:
        assert lil_time <= max_expected_time, "LIL matrix performance issue."
        assert dok_time <= max_expected_time, "DOK matrix performance issue."
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        test()
        print("Test passed successfully, no performance issue detected.")
    except AssertionError:
        # As instructed, exit with code 0 even when assertion fails
        exit(0)
```
This script checks whether `randomized_svd` performance on `lil_matrix` and `dok_matrix` exceeds an arbitrary threshold set as 5 times the duration taken by `randomized_svd` for a `csr_matrix`. It would print a stack trace and still exit with code 0 when the assertion fails, in accordance with the requirements specified.