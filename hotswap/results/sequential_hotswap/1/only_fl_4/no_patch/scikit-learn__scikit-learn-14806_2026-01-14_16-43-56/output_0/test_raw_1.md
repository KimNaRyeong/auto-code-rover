```python
import numpy as np

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
    try:
        from sklearn.impute import IterativeImputer
        # Set up the iterative imputer with max_iter=10 and verbosity off
        imp = IterativeImputer(max_iter=10, verbose=0)

        # First scenario: The imputer is trained on data without missing values in the second feature
        imp.fit([[1, 2], [3, 6], [4, 8], [10, 20], [np.nan, 22], [7, 14]])
        X_test_1 = [[np.nan, 4], [6, np.nan], [np.nan, 6], [4, np.nan], [33, np.nan]]
        result_1 = np.round(imp.transform(X_test_1))

        # Second scenario: Adjusting so the imputer sees missing values in both features during training
        imp.fit([[1, 2], [3, 6], [4, 8], [10, 20], [np.nan, 22], [7, np.nan]])
        X_test_2 = [[np.nan, 4], [6, np.nan], [np.nan, 6], [4, np.nan], [33, np.nan]]
        result_2 = np.round(imp.transform(X_test_2))

        # Assert that the behavior differs, indicating the conditional issue is present.
        assert not np.array_equal(result_1[:, 1], result_2[:, 1]), "Issue: Imputation behaves unexpectedly."

    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        reproduce_issue()
        print("The issue appears to be fixed, no AssertionError raised.")
        exit(0)  # Exit with code 0 to indicate success/no issue found.
    except AssertionError:
        print("AssertionError raised, indicating the issue is present.")
        exit(1)  # Exit with code 1 to signal the presence of the issue.
```

This script attempts to specifically reproduce the issue concerning the `IterativeImputer`'s behavior with missing values in `scikit-learn`. It includes functionality to raise an `AssertionError` when the issue described (i.e., the imputation method falls back to mean imputation unexpectedly) is detected, alongside printing a stack trace for diagnosing precisely where the error occurred. Exiting with code 0 indicates that the issue is resolved (or not present), while exit code 1 signals the detection of the problem as outlined in the provided description.