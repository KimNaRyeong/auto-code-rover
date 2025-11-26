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

def main():
    X = np.array([[0,0,0],[0,0,0],[1,1,1]])
    X_sparse = sparse.csc_matrix(X)
    X_sparse[0] = 0    # explicit zeros in first row

    imp = SimpleImputer(missing_values=0, strategy='mean')
    result = imp.fit_transform(X_sparse)

    expected_result = np.array([[1., 1., 1.],
                                [1., 1., 1.],
                                [1., 1., 1.]])
    
    try:
        assert np.allclose(result, expected_result)
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
