# reproducer.py
def main():
    try:
        import scipy.sparse as sp
        from sklearn.utils.sparsefuncs import min_max_axis

        X = sp.csc_matrix([[1, 2], [3, 4]])
        X.indptr = X.indptr.astype('int64')

        Y = sp.csr_matrix([[1, 2], [3, 4]])
        Y.indptr = Y.indptr.astype('int64')

        # Perform the operations that are expected to work
        result_y = min_max_axis(Y, 0)
        result_x = min_max_axis(X, 0)

        # If the issue is present, the following lines will not be reached for X.
        # Assert expected results to validate correct execution when the issue is fixed.
        assert (result_y[0] == [1, 2]).all() and (result_y[1] == [3, 4]).all(), \
            "Incorrect result for Y"
        assert (result_x[0] == [1, 2]).all() and (result_x[1] == [3, 4]).all(), \
            "Incorrect result for X"
    
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("The issue as described is present.")

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

if __name__ == "__main__":
    main()
