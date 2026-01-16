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

def main():
    import numpy as np
    from scipy import sparse
    from sklearn.impute import SimpleImputer

    X = np.array([[0, 0, 0], [0, 0, 0], [1, 1, 1]])
    X_sparse = sparse.csc_matrix(X)
    X_sparse[0] = 0  # Explicit zeros in first row

    imp = SimpleImputer(missing_values=0, strategy='mean')
    transformed = imp.fit_transform(X_sparse)

    expected_result = np.array([[1., 1., 1.],
                                [1., 1., 1.],
                                [1., 1., 1.]])

    try:
        assert np.array_equal(transformed.toarray() if sparse.issparse(transformed) else transformed, expected_result), "SimpleImputer gives wrong result on sparse matrix with explicit zeros"
    except AssertionError as e:
        print_stacktrace(e)
        raise e

if __name__ == '__main__':
    main()
```

Before running this script, ensure that you have installed the required packages (`numpy`, `scipy`, and `scikit-learn`) in your Python environment. This can generally be done using pip by running the command `pip install numpy scipy scikit-learn` in your terminal. 

This script will:

1. Import required libraries.
2. Create a sparse matrix `X_sparse` with explicit zeros in the first row.
3. Initialize a `SimpleImputer` object to replace zeros with the mean of the column.
4. Attempt to transform `X_sparse` using the imputer.
5. Compare the transformed matrix to the expected result, wherein each zero in the original matrix should have been replaced by the column mean.
6. If the actual result does not match the expected result, it raises an `AssertionError` and prints a stack trace, indicating the bug is present.
7. If no assertion is raised, the script exits with code 0, indicating the issue has been fixed.