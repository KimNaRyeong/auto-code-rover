Here is the reproducer script:

```python
import numpy as np
from sklearn.calibration import CalibratedClassifierCV
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler

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

def reproduce_issue():
    X = np.array([[[2.3, 5.4], [4.4, 5.6]], [[7.5, 1.2], [4.4, 5.6]]])
    y = np.array([[0], [1]])
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X.reshape(-1, 3)).reshape(X.shape)
    
    clf = SVC(kernel='linear')
    calibrated_clf = CalibratedClassifierCV(clf, method='isotonic', cv=2)
    
    try:
        calibrated_clf.fit(X_scaled, y)
    except AssertionError as e:
        print_stacktrace(e)
        exit(0)

if __name__ == "__main__":
    reproduce_issue()
```

This script creates a 3D array `X` and then scales it using `StandardScaler`. Then it trains an SVM classifier with isotonic calibration. If the issue is present, it should raise an `AssertionError`, which will be caught by the script and printed to the console along with the stack trace.