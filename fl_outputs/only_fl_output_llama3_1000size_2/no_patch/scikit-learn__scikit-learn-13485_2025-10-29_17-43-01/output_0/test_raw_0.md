Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV

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
    np.random.seed(0)
    X = np.random.rand(10, 2)
    y = np.random.randint(0, 2, size=10)
    clf = RandomForestClassifier(n_estimators=100)
    calibrated_clf = CalibratedClassifierCV(clf, method='isotonic', cv=5)

    # This should raise an AssertionError
    try:
        calibrated_clf.fit(X, y)
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script creates a random forest classifier and then attempts to calibrate it using `CalibratedClassifierCV`. The issue should be reproduced by trying to fit the calibrated classifier with 3D input data.