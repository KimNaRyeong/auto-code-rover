Below is the `reproducer.py` script tailored to reproduce the described issue. This script attempts to fit a `RidgeCV` model with integer `alphas`. It raises an `AssertionError` if the error occurs as described, capturing and printing the traceback of the exception. It exits with code 0 if the issue doesn't occur (i.e., if the issue is fixed and no exception is raised).

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

try:
    from sklearn.linear_model import RidgeCV
    from sklearn.datasets import make_regression

    # Generate a random regression problem
    X, y = make_regression()

    # Fit RidgeCV with integer alphas
    ridge = RidgeCV(alphas=[1, 10, 100, 1000]).fit(X, y)

    # If the block above passes without raising a ValueError, we consider the issue fixed.
    # Thus, the script should exit with 0 indicating success/no error.
    print("Issue is fixed, exiting with code 0.")
    exit(0)

except ValueError as e:
    # If the specific error described in the issue is caught, we print the stack trace.
    print_stacktrace(e)
    # Raising an AssertionError to indicate the issue is present.
    raise AssertionError("The ValueError issue is present.")

```

To execute this script, save it to the root directory of your project as described, and run it using:

```sh
python3 reproducer.py
```

Based on your instructions, if the issue is present, the `AssertionError` will be raised, along with a printed stack trace detailing the lines of code that led to the exception. If the issue has been resolved (for instance, if the `RidgeCV` internally handles integer `alphas` without throwing a `ValueError`), the script will print "Issue is fixed, exiting with code 0." and exit accordingly.