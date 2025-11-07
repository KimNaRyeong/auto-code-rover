```python
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

def main():
    import numpy as np
    from sklearn import datasets
    from sklearn.ensemble import GradientBoostingRegressor

    boston = datasets.load_boston()
    X, Y = (boston.data, boston.target)

    n_estimators = 720  # Known issue after 712 estimators
    params = {'n_estimators': n_estimators, 'max_depth': 6, 'learning_rate': 0.1}
    clf = GradientBoostingRegressor(**params)
    clf.fit(X, Y)

    feature_importance_sum = np.sum(clf.feature_importances_)
    print("At n_estimators = %i, feature importance sum = %f" % (n_estimators, feature_importance_sum))

    assert feature_importance_sum == 1.0, f"Feature importance sum is not equal to 1.0 but is {feature_importance_sum}"

    # Verifying at every stage to more accurately pinpoint the issue
    for i, tree in enumerate(clf.estimators_):
        current_sum = np.sum(tree[0].feature_importances_)
        try:
            assert current_sum == 1.0, f"At n_estimators = {i}, feature importance sum = {current_sum}"
        except AssertionError as e:
            print(f"Issue found at n_estimators = {i}")
            print_stacktrace(e)
            break  # Stop after the first failure to avoid redundant output

if __name__ == "__main__":
    main()
```

This script tries to reproduce the issue where feature importance sums do not equal 1 with a GradientBoostingRegressor. If the issue is present, the script will raise an `AssertionError` and print out a detailed stack trace using the `print_stacktrace` function. The try-except block around the assertion inside the loop allows the script to catch and print the issue as soon as it appears without processing the remaining estimators unnecessarily. The script will exit with code 0 when the issue is fixed, assuming no uncaught exceptions are raised.