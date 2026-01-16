```python
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


def main():
    try:
        X = np.array([[0, 0, 0], [0, 0, 0], [1, 1, 1]])
        X_sparse = sparse.csc_matrix(X)
        X_sparse[0, :] = 0  # explicit zeros in first row

        imp = SimpleImputer(missing_values=0, strategy='mean')
        X_imputed = imp.fit_transform(X_sparse)
        expected_result = np.array([[1., 1., 1.],
                                    [1., 1., 1.],
                                    [1., 1., 1.]])
                                    
        # Assert the expected result matches the actual result
        assert np.array_equal(X_imputed, expected_result), "Imputation did not produce the expected result."

        print("No issue detected.")
    except AssertionError as e:
        print_stacktrace(e)
        raise e  # Re-raise the exception to make the script exit due to the assertion failure.


if __name__ == "__main__":
    main()
```

This Python script is designed to reproduce the mentioned issue with `SimpleImputer` and sparse matrices. When executed, it will attempt to impute missing values (in this case, zeros) in a sparse matrix using the mean strategy. It then compares the result with the expected output. If the issue described is present, the script will cause an `AssertionError` and print a detailed stack trace. Note that as per the requirement, the script should exit with code 0 when the issue is fixed; however, the provided script will exit with an error state due to the assertion failure if the issue exists. To ensure it exits with code 0 when the problem is fixed, you could handle this case differently or simply rely on the lack of an error state as an indication of resolution.