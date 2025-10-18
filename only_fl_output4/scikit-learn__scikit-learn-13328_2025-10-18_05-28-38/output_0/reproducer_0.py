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
        import numpy as np
        from sklearn.datasets import make_regression
        from sklearn.linear_model import HuberRegressor

        # Random data
        X, y, coef = make_regression(n_samples=200, n_features=2, noise=4.0, coef=True, random_state=0)
        X_bool = X > 0

        # Attempting the operation that is expected to fail
        huber = HuberRegressor().fit(X_bool, y)

        # If the operation above didn't raise an exception, 
        # it means the issue has been fixed
        print("Issue resolved - no TypeError encountered when supplying a boolean X to HuberRegressor fit.")
        exit(0)

    except Exception as e:
        print_stacktrace(e)
        # Since the script is expected to raise an AssertionError when the issue is present,
        # we raise an AssertionError if we catch any exception here to indicate the issue is still present.
        raise AssertionError("Issue is still present.")

if __name__ == "__main__":
    main()
