 I apologize for the mistake in my previous response. Here's the corrected `reproducer.py` script:
```python
import numpy as np
from sklearn import datasets
from sklearn.ensemble import GradientBoostingRegressor
import sys
import traceback

def print_stacktrace(e: Exception):
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
    # Note: From 712 onwards, the feature importance sum is less than 1

    params = {'n_estimators': n_estimators, 'max_depth': 6, 'learning_rate': 0.1}
    clf = GradientBoostingRegressor(**params)
    clf.fit(X, Y)

    feature_importance_sum = np.sum(clf.feature_importances_)
    assert np.isclose(feature_importance_sum, 1.0), f"At n_estimators = {n_estimators}, feature importance sum = {feature_importance_sum}"

    for i, tree in enumerate(clf.estimators_):
        feature_importance_sum = np.sum(tree[0].feature_importances_)
        assert np.isclose(feature_importance_sum, 1.0), f"At n_estimators = {i}, feature importance sum = {feature_importance_sum}"

if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
```
This script should raise an `AssertionError` with a stack trace when executed with `python3 reproducer.py`, indicating that the feature importance sum is not equal to 1.0. This reproduces the issue reported in the original bug report.