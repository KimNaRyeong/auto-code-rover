Here is the `reproducer.py` file to reproduce the issue:
```
import scipy.sparse as sp
from sklearn.utils.sparsefuncs import min_max_axis

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
    X = sp.csc_matrix([[1,2],[3,4]])
    X.indptr = X.indptr.astype('int64')

    Y = sp.csr_matrix([[1,2],[3,4]])
    Y.indptr = Y.indptr.astype('int64')

    print(min_max_axis(Y, 0))
    result_X = min_max_axis(X, 0)
    expected_result_X = (array([1, 2], dtype=int32), array([3, 4], dtype=int32))
    assert result_X == expected_result_X, "min_max_axis failed on csc matrix with int64 indptr"
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue is present") from e
```
This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue. It will exit with code 0 when the issue is fixed.