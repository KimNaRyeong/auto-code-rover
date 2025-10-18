```python
# reproducer.py
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

def check_feature_importance_sum():
    boston = datasets.load_boston()
    X, Y = (boston.data, boston.target)

    n_estimators = 720
    params = {'n_estimators': n_estimators, 'max_depth': 6, 'learning_rate': 0.1}
    clf = GradientBoostingRegressor(**params)
    clf.fit(X, Y)

    feature_importance_sum = np.sum(clf.feature_importances_)
    try:
        assert feature_importance_sum == 1.0, f"Sum of feature importances is not equal to 1, was {feature_importance_sum}"
    except AssertionError as e:
        print_stacktrace(e)
        raise e

if __name__ == "__main__":
    try:
        check_feature_importance_sum()
    except AssertionError:
        exit(1) # exit with error if the assertion failed
    exit(0) # exit successfully if the issue is fixed
```