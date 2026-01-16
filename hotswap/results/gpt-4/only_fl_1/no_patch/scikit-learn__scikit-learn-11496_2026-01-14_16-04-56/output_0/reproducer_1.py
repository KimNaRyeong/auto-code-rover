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

def test_imputer_with_sparse_matrix():
    X = np.array([[0, 0, 0], [0, 0, 0], [1, 1, 1]])
    X_sparse = sparse.csc_matrix(X)
    # Adjusting to correctly modify a sparse matrix
    X_sparse[0, :] = 0  # Attempt to set explicit zeros in first row (this way might not change the matrix structurally in an intended manner due to scipy.sparse limitations)
    
    imp = SimpleImputer(missing_values=0, strategy='mean')
    transformed_X = imp.fit_transform(X_sparse)

    expected_result = np.array([[1., 1., 1.],
                                [1., 1., 1.],
                                [1., 1., 1.]])
    
    try:
        # Since `transformed_X` is directly a numpy array after `fit_transform`, no need to call `toarray` on it
        assert np.array_equal(transformed_X, expected_result), "Imputer result mismatch."
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        test_imputer_with_sparse_matrix()
    except Exception as e:
        exit(1) # Exits with code 1 to indicate failure in reproducing the expected results correctly
    exit(0) # Exits with code 0 indicating successful reproduction or no issue found
