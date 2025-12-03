import sys
import numpy as np
import scipy.sparse as sp

def min_max_axis_csc(X, axis):
    major_index = np.flatnonzero(X.indptr[1:] - X.indptr[:-1])
    minor_index = X.indices[major_index]
    value = X.data[major_index]
    if axis == 0:
        major_index, value = np.minor_axis_reduceat(major_index, X.indptr)
    else:
        major_index, value = np.minor_axis_reduceat(minor_index, X.indptr)
    return major_index, value

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

try:
    X = sp.csc_matrix(np.random.rand(1000, 1000)).astype(np.float64)
    X.indptr = X.indptr.astype('int64')
    min_max_axis_csc(X, 0)
except Exception as e:
    print_stacktrace(e)
    assert False, "Issue reproduced"

try:
    X = sp.csc_matrix(np.random.rand(1000, 1000)).astype(np.float64)
    X.indptr = X.indptr.astype('int32')
    min_max_axis_csc(X, 0)
except Exception as e:
    print_stacktrace(e)
    assert False, "Issue reproduced"

try:
    X = sp.csc_matrix(np.random.rand(1000, 1000)).astype(np.float64)
    X.indptr = X.indptr.astype('int64')
    min_max_axis_csc(X, 1)
except Exception as e:
    print_stacktrace(e)
    assert False, "Issue reproduced"

assert True, "Test passed"
