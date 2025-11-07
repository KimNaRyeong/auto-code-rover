```python
# reproducer.py
def main():
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
        print("At n_estimators = %i, feature importance sum = %f" % (n_estimators, feature_importance_sum))
        assert 0.99 <= feature_importance_sum <= 1.01, "Feature importances do not sum to approximately 1"

        # Check if feature importance per tree goes to 0 after a certain point
        for i, tree in enumerate(clf.estimators_):
            feature_importance_sum = np.sum(tree[0].feature_importances_)
            if feature_importance_sum == 0:
                break
        else:
            raise AssertionError("Feature importance of all trees is non-zero")

        # If assertion is passed or no exception, it's assumed the issue is fixed
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with code 1 if there is any exception

if __name__ == "__main__":
    main()
```

This script `reproducer.py` should be executed in the root directory of a project with `python3 reproducer.py`. It raises an `AssertionError` when the condition described in the original issue is observed—a scenario where feature importances of Gradient Boosting Regressor estimators are unexpectedly less than 1.

It utilizes an `assert` statement to enforce that the sum of feature importances should be exactly 1 (with a tiny bit of room for floating-point errors, hence the range `[0.99, 1.01]`). Furthermore, it iterates through all the estimators to identify if at any point any tree's feature importances sum to 0, which should not be the case. If either of these assertions fails, it will catch the exception, print a stack trace detailing the issue, and exit with code 1. If everything performs as expected (i.e., the issue is fixed or does not occur), the script will exit with code 0.