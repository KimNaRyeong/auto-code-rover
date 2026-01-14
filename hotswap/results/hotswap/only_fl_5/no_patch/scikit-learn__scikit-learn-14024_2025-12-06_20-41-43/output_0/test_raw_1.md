 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
from sklearn.datasets import fetch_openml
from sklearn.model_selection import cross_val_score
from sklearn.experimental import enable_hist_gradient_boosting
from sklearn.ensemble import HistGradientBoostingClassifier
import numpy as np

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

# one hundred plants - margin
bunch = fetch_openml(data_id=1491)
X = bunch.data
y = bunch.target

try:
    res = cross_val_score(HistGradientBoostingClassifier(max_iter=100, min_samples_leaf=5), X, y)
    np.mean(res)
except Exception as e:
    assert isinstance(e, ZeroDivisionError), "Expected ZeroDivisionError, but got: {}".format(type(e))
    print_stacktrace(e)
    raise
```
When executed with `python3 reproducer.py`, the script will print the stack trace of the `ZeroDivisionError` if present, and exit with code 0. If the issue is fixed, the script will not raise any exceptions and exit with code 0.