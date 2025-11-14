Here is the standalone Python file `reproducer.py` to reproduce the issue:
```python
import numpy as np
from sklearn.mixture import GaussianMixture

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

X = np.random.rand(1000, 10)
for random_state in range(100):
    gm1 = GaussianMixture(n_components=2, n_init=1, random_state=random_state).fit(X)
    gm2 = GaussianMixture(n_components=2, n_init=10, random_state=random_state).fit(X)
    if gm2.lower_bound_ <= gm1.lower_bound_:
        print("Assertion failed!")
        raise AssertionError
    print_stacktrace(AssertionError)
```
This script reproduces the issue by running 100 iterations of Gaussian mixture models with different initializations and checking that the lower bound of the model with `n_init=10` is greater than or equal to the lower bound of the model with `n_init=1`. If the assertion fails, it prints an error message and raises an `AssertionError`, which should print a stack trace.