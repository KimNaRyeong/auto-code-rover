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
    from sklearn.preprocessing import SplineTransformer
    from scipy.sparse import issparse

    # Define input matrix
    X = np.arange(6).reshape(6, 1)

    # Initialize SplineTransformer with sparse output option
    try:
        spline = SplineTransformer(degree=2, n_knots=3, sparse=True)
        transformed_X = spline.fit_transform(X)

        # Check if the output is sparse, raise AssertionError if not
        if not issparse(transformed_X):
            raise AssertionError("SplineTransformer did not produce sparse output as expected.")
    except Exception as e:
        print_stacktrace(e)
        exit(1) # Exits with error if an exception is caught

    # If no exceptions and checks pass
    print("Issue is fixed.")
    exit(0) # Exits with no error 

if __name__ == '__main__':
    main()
```
This script tries to utilize the `SplineTransformer` with a hypothetical `sparse=True` flag aiming to enable the return of a sparse matrix output, according to the described issue. It checks if the output is a sparse matrix, and raises an `AssertionError` if it isn't. In case any exceptions occur during this process, a detailed stack trace is printed using the `print_stacktrace` function, and the script exits with an error code (1). If no issue is detected, the script exits with code 0 indicating the absence of the problem.