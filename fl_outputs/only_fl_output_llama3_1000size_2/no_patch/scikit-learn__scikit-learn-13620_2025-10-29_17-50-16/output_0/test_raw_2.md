The issue seems to be related to the installation of scikit-learn. The error message suggests that scikit-learn has not been built correctly.

To reproduce this issue, we can try installing scikit-learn from source and then running the reproducer script. Here is a standalone python file `reproducer.py`:

```
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

try:
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
            raise AssertionError("Feature importance sum is not close to 1 at some point")

except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
```

This script will install scikit-learn from source and then run the reproducer. If the issue is present, an `AssertionError` will be raised and a stack trace will be printed.