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

        # Generate random data
        X, y, coef = make_regression(n_samples=200, n_features=2, noise=4.0, coef=True, random_state=0)
        X_bool = X > 0

        # Try to fit HuberRegressor
        huber = HuberRegressor()
        huber.fit(X_bool, y)  # This line is expected to cause the TypeError

        # If the exception is not raised, the issue is assumed to be fixed.
        print("Issue does not reproduce; it appears to be fixed.")
        exit(0)

    except Exception as e:
        print_stacktrace(e)
        # Now, we should assert False to make sure to indicate error when the exception is caught
        assert False, "The issue reproduced with an error."

if __name__ == "__main__":
    main()
