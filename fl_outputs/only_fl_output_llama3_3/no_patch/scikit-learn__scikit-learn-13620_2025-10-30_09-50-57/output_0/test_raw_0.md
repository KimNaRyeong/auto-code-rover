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
    if feature_importance_sum < 1:
        raise AssertionError("Feature importance sum is less than 1")

    for i, tree in enumerate(clf.estimators_):
        feature_importance_sum = np.sum(tree[0].feature_importances_)
        print(f"At n_estimators = {i}, feature importance sum = {feature_importance_sum}")

try:
    reproduce_issue()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue not reproduced. Feature importance sum is 1.")
exit(0)
```

This script will raise an `AssertionError` if the feature importance sum is less than 1, and it will print a stack trace of the issue. If the issue is not present (i.e., the feature importance sum is 1), it will print a success message and exit with code 0.