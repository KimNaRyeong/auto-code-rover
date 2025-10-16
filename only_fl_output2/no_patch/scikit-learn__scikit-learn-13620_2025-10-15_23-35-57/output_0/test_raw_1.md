```python
# reproducer.py
import numpy as np
from sklearn import datasets
from sklearn.ensemble import GradientBoostingRegressor
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)


def test_feature_importances_sum_to_one():
    boston = datasets.load_boston()
    X, Y = (boston.data, boston.target)

    n_estimators = 720
    params = {'n_estimators': n_estimators, 'max_depth': 6, 'learning_rate': 0.1}
    clf = GradientBoostingRegressor(**params)
    clf.fit(X, Y)

    feature_importance_sum = np.sum(clf.feature_importances_)
    if not np.isclose(feature_importance_sum, 1, atol=1e-3):
        raise AssertionError(f"Feature importance sum not close to 1 (sum={feature_importance_sum})")

    # Test for each tree's feature importance sum
    zero_sum_after_estimator_number = None
    for i, tree in enumerate(clf.estimators_):
        tree_importance_sum = np.sum(tree[0].feature_importances_)
        if tree_importance_sum == 0:
            zero_sum_after_estimator_number = i
            break

    if zero_sum_after_estimator_number is not None:
        raise AssertionError(f"Feature importance of tree drops to 0 after {zero_sum_after_estimator_number} estimators")

try:
    test_feature_importances_sum_to_one()
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
```

This `reproducer.py` script is designed to reproduce the described issue when feature importances in Gradient Boosting Regressor do not sum to 1, particularly after a certain number of estimators are trained. When executed in a project's root directory with `python3 reproducer.py`, it will conduct the necessary tests to validate the consistency of feature importance sums.

- **Test for Feature Importances Sum**: The script first fits a `GradientBoostingRegressor` model on the Boston housing dataset with a significant number of estimators. It then checks if the sum of feature importances is approximately 1, considering a small tolerance for floating-point arithmetic inaccuracies.

- **Test for Individual Trees' Feature Importances**: It iterates over each tree model within the gradient boosting ensemble to examine if there's a point where a tree's feature importances sum to 0, which should not normally occur.

An `AssertionError` is raised if any of the conditions fail, signaling the presence of the described issue. The custom `print_stacktrace` function provides detailed error context, aiming to aid in diagnosing the problem's source. The script exits with code 1 upon encountering an error, indicating failure, and exits with code 0 if no problems are found, signaling that the issue is either fixed or not present.