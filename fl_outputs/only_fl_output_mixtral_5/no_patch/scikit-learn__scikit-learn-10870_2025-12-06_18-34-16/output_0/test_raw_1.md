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
This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue. The script will also exit with code 0 when the issue is fixed.

The issue is that the `lower_bound_` attribute of the `GaussianMixture` object is not the maximum lower bound across all initializations, but just the lower bound of the last initialization. This can be fixed by adding the following line just before `return self` in `BaseMixture.fit()`:
```python
self.lower_bound_ = max_lower_bound
```
Additionally, the test that should have caught this bug is `test_init()` in `mixture/tests/test_gaussian_mixture.py`, but it just does a single test, so it had a 50% chance of missing the issue. It should be updated to try many random states.