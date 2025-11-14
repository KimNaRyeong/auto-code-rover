Here is the standalone Python file `reproducer.py` to reproduce the issue:
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

boston = datasets.load_boston()
X, Y = (boston.data, boston.target)

n_estimators = 720
params = {'n_estimators': n_estimators, 'max_depth': 6, 'learning_rate': 0.1}
clf = GradientBoostingRegressor(**params)
clf.fit(X, Y)

feature_importance_sum = np.sum(clf.feature_importances_)
print("At n_estimators = %i, feature importance sum = %f" % (n_estimators , feature_importance_sum))

try:
    assert np.isclose(feature_importance_sum, 1.0), "Feature importance sum is not close to 1"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
```
This script will raise an `AssertionError` when the feature importance sum is not close to 1, and print a stack trace of the issue. If the issue is fixed, it will exit with code 0.