Here is the `reproducer.py` file to reproduce the issue:
```
```python
import numpy as np
from sklearn.calibration import CalibratedClassifierCV
from sklearn.base import BaseEstimator

# Define a simple classifier that returns a decision function
class SimpleClassifier(BaseEstimator):
    def fit(self, X, y):
        return self
    
    def predict(self, X):
        # Return a decision function (not probabilities)
        return np.random.rand(X.shape[0])

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

# Create a 3D input array
pairs = np.array([[[2.3, 5.4], [4.4, 5.6]], [[7.5, 1.2], [4.4, 5.6]]])

try:
    # Try to use CalibratedClassifierCV with the 3D input array
    clf = SimpleClassifier()
    calibrated_clf = CalibratedClassifierCV(clf)
    calibrated_clf.fit(pairs, np.random.rand(pairs.shape[0]))
except ValueError as e:
    print_stacktrace(e)
    assert "array must be 2-dimensional" in str(e), "Issue not reproduced"
else:
    print("Issue fixed!")
```
This script defines a simple classifier that returns a decision function, creates a 3D input array, and tries to use `CalibratedClassifierCV` with this input. If the issue is present, it should raise a `ValueError` with a message indicating that the input array must be 2-dimensional. The script catches this exception, prints the stack trace using the provided function, and asserts that the error message contains the expected text. If the issue is fixed, the script simply prints "Issue fixed!" and exits with code 0.