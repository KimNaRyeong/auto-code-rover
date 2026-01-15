# reproducer.py
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

def test(X, seed=42):
    try:
        start_time = time.time()
        U, S, VT = randomized_svd(X, 50, random_state=seed)
        end_time = time.time()
        return end_time - start_time
    except Exception as e:
        print_stacktrace(e)
        # If there is any exception including timeout, this will ensure the script fails.
        sys.exit(1)

def main():
    np.random.seed(42)
    X = np.random.normal(0,1,[1000,1000]) * np.random.poisson(0.1, [1000,1000])
    X = sp.csr_matrix(X)

    # Define different sparse matrix formats
    matrix_formats = ['csr', 'csc', 'bsr', 'coo', 'lil', 'dok']
    times = {}

    # Loop through formats and calculate time for each format
    for fmt in matrix_formats:
        X_fmt = getattr(sp, f"{fmt}_matrix")(X)
        duration = test(X_fmt)
        times[fmt] = duration
        print(f"Time for {fmt}_matrix: {duration:.3f} seconds")

    # Checking if dok_matrix or lil_matrix take more than expected time
    allowed_ratio = 10  # Threshold for acceptable performance
    csr_time = times['csr']
    for fmt in ['dok', 'lil']:
        if times[fmt] > allowed_ratio * csr_time:
            raise AssertionError(f"{fmt}_matrix is significantly slower than expected.")

if __name__ == "__main__":
    try:
        main()
        sys.exit(0)  # Exit code 0 when no issue is found
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit code 1 indicates the issue is present
