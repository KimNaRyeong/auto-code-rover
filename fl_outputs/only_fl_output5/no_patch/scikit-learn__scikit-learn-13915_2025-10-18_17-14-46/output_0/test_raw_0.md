```python
# reproducer.py
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

    # Creating the matrices
    X = sp.csc_matrix([[1,2],[3,4]])
    X.indptr = X.indptr.astype('int64')

    Y = sp.csr_matrix([[1,2],[3,4]])
    Y.indptr = Y.indptr.astype('int64')

    # Expected output
    expected_output = (array([1, 2], dtype=int32), array([3, 4], dtype=int32))

    try:
        # Testing CSR matrix
        csr_output = min_max_axis(Y, 0)
        assert csr_output == expected_output, "CSR matrix test failed."

        # Testing CSC matrix
        csc_output = min_max_axis(X, 0)
        assert csc_output == expected_output, "CSC matrix test failed."

        # If both assertions pass, the issue is fixed, and we exit with code 0.
        print("Issue resolved.")
        exit(0)

    except Exception as e:
        print_stacktrace(e)
        # Raising AssertionError if the test fails to indicate the presence of the issue.
        raise AssertionError("Test failed due to an error.")

if __name__ == "__main__":
    test_min_max_axis()
```

This Python script checks for the issue described: `TypeError` when `min_max_axis` is called on a large CSC matrix with `indptr.dtype` as `int64` on 32-bit Windows versions. The script uses `print_stacktrace` to print the stack trace with line numbers for any exceptions that occur. It asserts the expected behavior, and if the assertion fails or an exception is raised, it catches the exception, prints the stack trace, and then raises an `AssertionError`. If the script executes without any exceptions or assertions failing, it concludes that the issue is resolved and exits with code 0, indicating success.