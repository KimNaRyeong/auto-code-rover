Here is the reproducer script:

```python
import numpy as np
import scipy.sparse as sp
from sklearn.utils.extmath import randomized_svd
import timeit
import traceback
import sys

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

try:
    np.random.seed(42)
    X = np.random.normal(0,1,[1000,1000]) * np.random.poisson(0, [1000,1000])
    X = sp.dok_matrix(X)
    start_time = timeit.default_timer()
    for _ in range(50):
        test(X)
    end_time = timeit.default_timer()
    if end_time - start_time > 1.5:  # adjust this threshold as needed
        raise AssertionError("Issue present")
except Exception as e:
    print_stacktrace(e)

if __name__ == "__main__":
    python3 reproducer.py