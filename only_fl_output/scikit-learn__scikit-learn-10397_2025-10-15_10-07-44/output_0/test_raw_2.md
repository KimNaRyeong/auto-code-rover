Certainly, creating a standalone Python script named `reproducer.py` to specifically catch the reported issue and follow your instructions will look something like this:

```python
# reproducerer.py

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

def test_issue():
    from sklearn.linear_model import RidgeCV
    from sklearn.datasets import make_regression

    X, y = make_regression()
    try:
        ridge = RidgeCV(alphas=[1, 10, 100, 1000]).fit(X, y)
        # If we reach this point without an error, the test did not find the issue.
        print("No issue detected with integer alphas in RidgeCV.")
        return True
    except ValueError as e:
        if "Integers to negative integer powers are not allowed" in str(e):
            print("Found the issue with integer alphas in RidgeCV.")
            print_stacktrace(e)
            return False
        else:
            # An unexpected error occurred which is not the one we're looking for.
            print("An unexpected error occurred.")
            print_stacktrace(e)
            return False

if __name__ == "__main__":
    if not test_issue():
        raise AssertionError("The issue is present.")
    # If the script did not find the issue (i.e., it executes successfully without errors),
    # it exits with code 0 indicating the issue has been fixed or does not exist.
```

This script attempts to reproduce the identified issue concerning the use of integers as alphas in the `RidgeCV` estimator from `scikit-learn`. When executed, the script:

- Runs the test function `test_issue`, which:
  - Instantiates `RidgeCV` with a list of integer `alphas`.
  - If the problematic behavior is observed (a `ValueError` about integers to negative integer powers), it reports that the issue is present, prints a stack trace, and the script raises an `AssertionError`.
  - If the error does not occur (implying either the issue has been fixed or the setup does not exhibit the problem), it reports no issues detected.
- Exits with code 0 if the issue is not detected, indicating the test passed successfully without catching the reported problem.

To use this script, simply place it in the root directory of your project and execute it using the command you mentioned (`python3 reproducer.py`).