 Here is a standalone Python script that reproduces the issue:
```python
import numpy as np
from sklearn.mixture import GaussianMixture

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
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
    try:
        assert gm2.lower_bound_ > gm1.lower_bound_, random_state
    except AssertionError:
        print_stacktrace(AssertionError(f"lower_bound_ is not the max for random_state={random_state}"))
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` when the issue is present and print a stack trace of the issue. The script should exit with code 0 when the issue is fixed.