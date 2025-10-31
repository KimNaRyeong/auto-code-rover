Here is the reproducer script:

```python
import numpy as np
from sklearn import datasets
from sklearn.ensemble import GradientBoostingRegressor
import sys
import traceback

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
    boston = datasets.load_boston()
    X, Y = (boston.data, boston.target)

    n_estimators = 720
    params = {'n_estimators': n_estimators, 'max_depth': 6, 'learning_rate': 0.1}
    clf = GradientBoostingRegressor(**params)
    try:
        clf.fit(X, Y)
        feature_importance_sum = np.sum(clf.feature_importances_)
        if not np.isclose(feature_importance_sum, 1):
            raise AssertionError("Feature importance sum is not close to 1")
    except Exception as e:
        print_stacktrace(e)

if __name__ == "__main__":
    reproduce_issue()
```

This script will run the Gradient Boosting Regressor with the given parameters and check if the feature importance sum is close to 1. If it's not, an `AssertionError` will be raised and the stack trace will be printed.