Here's the `reproducer.py` Python file you requested. This script will raise an `AssertionError` when it detects the issue as described, by checking for the specific exception raised when integer alphas are used in `RidgeCV`. It will print a stack trace of the issue if caught. When the underlying issue is fixed (either in a future version of `scikit-learn` or by internally casting alpha values to floats), the script should exit with code 0 without raising an exception.

```python
# reproducer.py

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

def test_ridge_cv_with_integers():
    from sklearn.linear_model import RidgeCV
    from sklearn.datasets import make_regression

    try:
        X, y = make_regression()
        ridge = RidgeCV(alphas=[1, 10, 100, 1000])
        ridge.fit(X, y)
        # If the code succeeds without an exception, we assume the issue is fixed
        print("Issue appears to be fixed.")
        exit(0)
    except ValueError as e:
        if "Integers to negative integer powers are not allowed" in str(e):
            print_stacktrace(e)
            # AssertionError to indicate the issue is present
            assert False, "The issue is present."
        else:
            # Reraise if it's a different ValueError
            raise

if __name__ == "__main__":
    test_ridge_cv_with_integers()
```

This script works as follows:
- It attempts to fit a `RidgeCV` model with integer values in the `alphas` parameter.
- If it encounters a `ValueError` specifically mentioning "Integers to negative integer powers are not allowed", it prints the stack trace using the provided function and raises an `AssertionError` indicating the issue is present.
- If the operation completes without encountering the specific `ValueError`, it prints a message suggesting the issue might be fixed and exits with code 0.
- If any other type of `ValueError` is caught, it is re-raised, ensuring that only the specific error of interest is caught and handled.