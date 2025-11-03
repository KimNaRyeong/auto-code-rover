The issue seems to be related to the installation of scikit-learn. The error message suggests that scikit-learn has not been built correctly.

Here's a revised version of the reproducer script:

```python
import numpy as np
from sklearn import datasets
from sklearn.ensemble import GradientBoostingRegressor

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
    try:
        boston = datasets.load_boston()
        X, Y = (boston.data, boston.target)

        n_estimators = 720
        params = {'n_estimators': n_estimators, 'max_depth': 6, 'learning_rate': 0.1}
        clf = GradientBoostingRegressor(**params)
        clf.fit(X, Y)

        feature_importance_sum = np.sum(clf.feature_importances_)
        if feature_importance_sum < 1:
            raise AssertionError("Feature importance sum is less than 1")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script will attempt to load the Boston housing dataset, create a Gradient Boosting Regressor model with the specified parameters, and then check if the feature importance sum is less than 1. If it is, an `AssertionError` will be raised, and the stack trace will be printed.

Please make sure that scikit-learn is installed correctly before running this script.