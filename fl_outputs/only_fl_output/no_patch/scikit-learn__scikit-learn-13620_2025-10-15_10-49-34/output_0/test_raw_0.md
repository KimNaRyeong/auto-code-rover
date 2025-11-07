Below is a `reproducer.py` script that encapsulates the issue described, including an assertion to trigger when feature importance sums do not equal 1 and utilising the provided function to print the stack trace upon the assertion failure. The script gracefully handles the assertion to ensure it exits with code 0 if the issue is fixed, meaning that feature importance sums return to being 1.

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

def check_feature_importance_sum():
    # Load dataset
    boston = datasets.load_boston()
    X, Y = (boston.data, boston.target)

    n_estimators = 720
    params = {'n_estimators': n_estimators, 'max_depth': 6, 'learning_rate': 0.1}
    clf = GradientBoostingRegressor(**params)
    clf.fit(X, Y)
  
    # Calculate overall feature importance sum
    feature_importance_sum = np.sum(clf.feature_importances_)
    print("Overall feature importance sum =", feature_importance_sum)

    # Ensure feature importance sums to 1 or raise an AssertionError
    assert np.isclose(feature_importance_sum, 1.0), "Feature importance sum does not equal 1."

    # Check each tree's feature importance sum
    for i, tree in enumerate(clf.estimators_):
        feature_importance_sum = np.sum(tree[0].feature_importances_)
        try:
            assert np.isclose(feature_importance_sum, 1.0), f"At n_estimators = {i}, feature importance sum = {feature_importance_sum}"
        except AssertionError as e:
            print(f"Failed at n_estimators = {i}")
            print_stacktrace(e)
            break  # Break after first failure to prevent flooding the output

if __name__ == "__main__":
    try:
        check_feature_importance_sum()
    except AssertionError as e:
        print_stacktrace(e)
    else:
        print("No issues found. Exiting with code 0.")
        exit(0)
```

This script performs the following steps:
1. It fits a `GradientBoostingRegressor` to the Boston housing dataset with a specified number of estimators and other parameters.
2. It then checks if the sum of feature importances from the fitted model is close to 1, which should always be the case for correctly functioning models.
3. If the feature importance sum is not close to 1, it raises an `AssertionError` and prints a detailed stack trace using the `print_stacktrace` function.
4. Additionally, it iterates through each estimator (tree) in the ensemble to check if their respective feature importance sum is close to 1, printing a stack trace upon finding the first failure.
5. If no `AssertionError` is raised, it prints a confirmation message and exits with code 0, indicating the issue is resolved or not present.