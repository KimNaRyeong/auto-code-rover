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

def test_min_max_axis():
    import scipy.sparse as sp
    from sklearn.utils.sparsefuncs import min_max_axis

    X = sp.csc_matrix([[1,2],[3,4]])
    X.indptr = X.indptr.astype('int64')

    Y = sp.csr_matrix([[1,2],[3,4]])
    Y.indptr = Y.indptr.astype('int64')

    expected_y_result = (array([1, 2], dtype=int32), array([3, 4], dtype=int32))
    expected_x_result = (array([1, 2], dtype=int32), array([3, 4], dtype=int32))

    try:
        y_result = min_max_axis(Y, 0)
        assert y_result == expected_y_result, "CSR matrix result does not match expected"

        x_result = min_max_axis(X, 0)
        assert x_result == expected_x_result, "CSC matrix result does not match expected"
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("An error occurred while testing min_max_axis with a CSC matrix.")

if __name__ == "__main__":
    try:
        test_min_max_axis()
    except AssertionError as e:
        print(e)
        sys.exit(1)
    print("Test passed")
    sys.exit(0)
```

This script checks the function `min_max_axis` on both CSR and CSC matrices after explicitly casting their `indptr` to `int64`, which replicates the conditions leading to the type error described. It uses assertions to ensure that both inputs produce expected results and gracefully handles exceptions by printing a comprehensive stack trace if an error occurs, particularly focusing on the scenario where the CSC matrix may trigger the error. The script exits with code 0 if the test passes, indicating the issue has been resolved, or exits with code 1 along with a printed stack trace if the issue persists.