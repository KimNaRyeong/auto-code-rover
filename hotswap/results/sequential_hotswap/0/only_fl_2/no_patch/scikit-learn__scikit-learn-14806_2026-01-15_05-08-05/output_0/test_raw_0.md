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

def test_iterative_imputer_behaviour():
    import numpy as np
    from sklearn.impute import IterativeImputer

    # First scenario with mean imputation
    imp1 = IterativeImputer(max_iter=10, verbose=0)
    imp1.fit([[1, 2], [3, 6], [4, 8], [10, 20], [np.nan, 22], [7, 14]])

    X_test1 = np.array([[np.nan, 4], [6, np.nan], [np.nan, 6], [4, np.nan], [33, np.nan]])

    result1 = np.round(imp1.transform(X_test1))

    expected_result1 = np.array([[2., 4.], [6., 12.], [3., 6.], [4., 12.], [33., 12.]])

    # Second scenario with iterative imputation
    imp2 = IterativeImputer(max_iter=10, verbose=0)
    imp2.fit([[1, 2], [3, 6], [4, 8], [10, 20], [np.nan, 22], [7, np.nan]])

    X_test2 = np.array([[np.nan, 4], [6, np.nan], [np.nan, 6], [4, np.nan], [33, np.nan]])

    result2 = np.round(imp2.transform(X_test2))

    expected_result2 = np.array([[2., 4.], [6., 12.], [3., 6.], [4., 8.], [33., 66.]])

    try:
        assert np.array_equal(result1, expected_result1), "First scenario results are incorrect."
        assert np.array_equal(result2, expected_result2), "Second scenario results are incorrect."
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        test_iterative_imputer_behaviour()
    except AssertionError:
        exit(1)
    exit(0)
```