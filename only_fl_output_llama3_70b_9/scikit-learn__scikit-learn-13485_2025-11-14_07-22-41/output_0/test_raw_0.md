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

if __name__ == "__main__":
    pairs = [[[2.3, 5.4], [4.4, 5.6]], [[7.5, 1.2], [4.4, 5.6]]]
    try:
        CalibratedClassifierCV(PairsClassifier()).fit(pairs)
    except ValueError as e:
        print_stacktrace(e)
        assert "array must be 2D" in str(e), "Issue not reproduced"
        print("Issue reproduced successfully")
        exit(1)
    else:
        print("Issue fixed, no error raised")
        exit(0)
```
This script defines a simple `PairsClassifier` estimator and tries to fit it using `CalibratedClassifierCV` with 3D input data. If the issue is present, it should raise a `ValueError` with a message containing "array must be 2D", which is caught and printed along with the stack trace. The script exits with code 1 if the issue is reproduced and code 0 if the issue is fixed.