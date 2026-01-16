# reproducer.py
import numpy as np
from scipy import sparse
from sklearn.impute import SimpleImputer

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

def test_simple_imputer_with_explicit_zeros():
    X = np.array([[0, 0, 0], [0, 0, 0], [1, 1, 1]])
    X_sparse = sparse.csc_matrix(X)
    X_sparse[0, :] = 0    # correct way to assign explicit zeros

    imp = SimpleImputer(missing_values=0, strategy='mean')
    transformed_X = imp.fit_transform(X_sparse)

    expected_result = np.array([[1., 1., 1.],
                                [1., 1., 1.],
                                [1., 1., 1.]])

    try:
        # Given that transformed_X is already a numpy array, no need for toarray()
        assert np.allclose(transformed_X, expected_result), "The SimpleImputer does not handle explicit zeros in sparse matrices correctly."
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        test_simple_imputer_with_explicit_zeros()
    except AssertionError:
        exit(1)  # Exit with code 1 when issue is present.
    exit(0)  # Exit with code 0 when issue is fixed.
