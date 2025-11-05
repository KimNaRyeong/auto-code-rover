Here is the reproducer script:

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
    boston = datasets.load_boston()
    X, Y = (boston.data, boston.target)

    n_estimators = 720
    params = {'n_estimators': n_estimators, 'max_depth': 6, 'learning_rate': 0.1}
    clf = GradientBoostingRegressor(**params)
    clf.fit(X, Y)

    feature_importance_sum = np.sum(clf.feature_importances_)
    if not np.isclose(feature_importance_sum, 1):
        raise AssertionError("Feature importance sum is not close to 1")

    for i, tree in enumerate(clf.estimators_):
        feature_importance_sum = np.sum(tree[0].feature_importances_)
        if not np.isclose(feature_importance_sum, 1):
            print_stacktrace(AssertionError(f"Feature importance sum at n_estimators {i} is not close to 1"))
            exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script will raise an `AssertionError` if the feature importance sum is not close to 1, and print a stack trace of the issue. If the issue is fixed, it will simply exit with code 0.