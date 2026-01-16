```python
# reproducer.py
import numpy as np
import scipy.sparse as sp
from sklearn.utils.extmath import randomized_svd
import timeit
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
    U, S, VT = randomized_svd(X, 50, random_state=seed)

try:
    np.random.seed(42)
    X = np.random.normal(0,1,[1000,1000]) * np.random.poisson(0.1, [1000,1000])

    # Convert X to different sparse matrix formats and test
    formats = ['csr', 'csc', 'bsr', 'coo', 'lil', 'dok']
    durations = {}
    
    for format in formats:
        sparse_func = getattr(sp, f"{format}_matrix")
        X_sparse = sparse_func(X)
        # Measure time of the test function
        duration = timeit.timeit(lambda: test(X_sparse), number=50)
        durations[format] = duration
        print(f"{format}_matrix: {duration:.2f} s")  # Output the duration for diagnostic purposes

    # Check if dok_matrix or lil_matrix take substantially longer than others
    ref_duration = min(durations.values())
    for format in ['dok', 'lil']:
        if durations[format] > 10 * ref_duration:
            raise AssertionError(f"{format}_matrix processing time is significantly longer.")

except Exception as e:
    print_stacktrace(e)
    # Make sure to exit with non-zero code if the exception is raised indicating the issue exists
    sys.exit(1)

# Exit with 0 if everything is fine
sys.exit(0)

```

This script takes the approach of measuring the time it takes to execute the `randomized_svd` function on different sparse matrix formats produced from the same dense matrix. It checks if the `dok_matrix` or `lil_matrix` data structures cause the function to take significantly more time (currently set to 10 times more than the fastest one) to process. If such a significant degradation in performance is detected, it raises an `AssertionError` and prints a stack trace to help identify where the issue originates.

Please note: The definition of "significantly longer" as being "10 times longer" is a bit arbitrary for the purposes of this script. Depending on the specific requirements or acceptable performance criteria of your application, you might adjust this threshold.