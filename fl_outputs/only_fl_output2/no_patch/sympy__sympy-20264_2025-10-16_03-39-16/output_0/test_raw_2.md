Certainly! Below is a standalone Python script named `reproducer.py` that follows your instructions. This script attempts to reproduce the specified issue and uses the provided `print_stacktrace` function to clearly display the stack trace when an exception occurs. It will raise an `AssertionError` if the script unexpectedly does not encounter the issue, indicating the issue might be fixed. Conversely, it should terminate normally if the issue is present and the expected `RecursionError` is raised.

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

def reproduce_issue():
    from sympy import Pow, Rational, latex
    try:
        # Attempt to reproduce the issue with specific sympy expression
        latex_expression = latex(Pow(Rational(1, 2), -1, evaluate=False))
    except RecursionError as e:
        # Print the stack trace if a RecursionError is caught
        print_stacktrace(e)
        # Exit with code 0 indicating the issue is reproduced successfully
        exit(0)
    # If the RecursionError was not raised as expected, it may indicate the issue has been resolved
    raise AssertionError("RecursionError was not raised. The issue might be fixed.")

if __name__ == "__main__":
    reproduce_issue()
```

This script checks for the occurrence of a `RecursionError` when converting a specific sympy expression to LaTeX. It respects the semantics outlined in your instructions, including the use and definition of `print_stacktrace` as well as conditionally raising `AssertionError` or exiting with code 0 based on the outcome of the test.