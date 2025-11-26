import numpy as np
import scipy.sparse as sp
from sklearn.utils.extmath import randomized_svd
import timeit

def test(X, seed=42):
    U, S, VT = randomized_svd(X, 50, random_state=seed)

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
    np.random.seed(42)
    X = np.random.normal(0, 1, [1000, 1000]) * np.random.poisson(0.1, [1000, 1000])

    matrices = [
        sp.csr_matrix(X),
        sp.csc_matrix(X),
        sp.bsr_matrix(X),
        sp.coo_matrix(X),
        sp.lil_matrix(X),
        sp.dok_matrix(X)
    ]

    max_allowed_time = 2  # seconds
    for matrix in matrices:
        start_time = timeit.default_timer()
        test(matrix)
        end_time = timeit.default_timer()
        elapsed_time = end_time - start_time
        if elapsed_time > max_allowed_time:
            raise AssertionError(f"randomized_svd is slow for {matrix.__class__.__name__} matrix")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        exit(1)

exit(0)
