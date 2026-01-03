 Here is a corrected standalone python file `reproducer.py` to reproduce the issue:
```python
import numpy as np
from sklearn.mixture import GaussianMixture

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == "__main__":
    X = np.random.rand(1000, 10)
    for random_state in range(100):
        gm1 = GaussianMixture(n_components=2, n_init=1, random_state=random_state).fit(X)
        gm2 = GaussianMixture(n_components=2, n_init=10, random_state=random_state).fit(X)
        try:
            assert gm2.lower_bound_ > gm1.lower_bound_, random_state
        except AssertionError as e:
            print_stacktrace(e)
            break
```
The script should raise an `AssertionError` when the issue is present and print a stack trace of the issue. The script should also exit with code 0 when the issue is fixed.

The issue is caused by the fact that the `lower_bound_` attribute of the `GaussianMixture` object is not updated to the maximum lower bound across all initializations when `n_init` is set to a value greater than 1. The `test_init()` function in `mixture/tests/test_gaussian_mixture.py` should be updated to try many random states to catch this bug.

The following line can be added to the `BaseMixture.fit()` function in `sklearn/mixture/_base.py` to fix the bug:
```python
self.lower_bound_ = max_lower_bound
```
This line should be added just before `return self` in the `BaseMixture.fit()` function. This will ensure that the `lower_bound_` attribute of the `GaussianMixture` object is updated to the maximum lower bound across all initializations.