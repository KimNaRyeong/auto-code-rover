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
