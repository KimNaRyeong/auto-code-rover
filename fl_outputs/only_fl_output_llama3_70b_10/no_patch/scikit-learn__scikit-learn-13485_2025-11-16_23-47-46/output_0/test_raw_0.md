Here is the `reproducer.py` file that reproduces the issue:
```
import numpy as np
from sklearn.calibration import CalibratedClassifierCV
from sklearn.base import BaseEstimator

class PairsClassifier(BaseEstimator):
    def fit(self, X, y=None):
        return self

    def predict(self, X):
        return np.zeros((X.shape[0],))

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

try:
    pairs = [[[2.3, 5.4], [4.4, 5.6]], [[7.5, 1.2], [4.4, 5.6]]]
    clf = CalibratedClassifierCV(PairsClassifier())
    clf.fit(pairs)
    assert False, "Expected ValueError"
except ValueError as e:
    print_stacktrace(e)
except Exception as e:
    print("Unexpected exception:", file=sys.stderr)
    print_stacktrace(e)
    raise
```
This script defines a simple `PairsClassifier` estimator that returns zeros for any input. It then tries to fit an instance of `CalibratedClassifierCV` with this estimator to the 3D input data. If the issue is present, it should raise a `ValueError` due to the `check_array` function in `CalibratedClassifierCV`. The script catches this exception, prints the stack trace using the provided `print_stacktrace` function, and exits with code 0. If any other exception occurs, it also prints the stack trace but raises the exception again.