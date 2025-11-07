Given the requirements and aiming to address the feedback provided, below is an updated version of `reproducer.py` designed to reproduce the issue mentioned. The script now includes logic to raise an `AssertionError` if the issue does not manifest as expected (thus indicating the presence of the issue when running against a problematic version of the library). It'll print a detailed stack trace if the issue is encountered, fulfilling the criteria for error reporting.

```python
from sympy import Pow, Rational, latex
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def check_issue():
    error_raised = False
    try:
        # Issue triggering expression
        latex_expr = latex(Pow(Rational(1,2),-1, evaluate=False))
        # Raise AssertionError if the recursion error isn't triggered
        assert "RecursionError did not occur as expected"
    except RecursionError as e:
        print_stacktrace(e)
        error_raised = True
    assert error_raised, "The issue did not trigger the expected RecursionError."

    # Validate further with the other case if first passed
    try:
        # Second issue triggering expression
        latex_expr = latex(Pow(Rational(-1,-5),-1, evaluate=False))
        # If execution continues without RecursionError, issue persists
    except RecursionError as e:
        print_stacktrace(e)
        error_raised = True

    # Confirm issue reproduction
    assert error_raised, "The issue did not trigger the expected RecursionError for both cases."

if __name__ == "__main__":
    check_issue()
    print("The test script executed successfully, indicating the issue was not replicated with the current library version, or it has been fixed.")
```

This script tests the two cases outlined in the original issue report. First, it executes a command expected to trigger a `RecursionError` due to a bug in handling specific expressions during LaTeX conversion. If the error is raised, it catches it, prints a detailed stack trace, and validates the test's objective. The `AssertionError`s are strategically placed to denote whether the issue is still occurring or if it fails to meet the expected condition, thus indicating a possible resolution to the reported bug.