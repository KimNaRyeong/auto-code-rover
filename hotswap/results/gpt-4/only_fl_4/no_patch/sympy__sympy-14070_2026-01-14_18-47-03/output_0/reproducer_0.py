# reproducer.py
import sys
from sympy import symbols, log, logcombine
from sympy.abc import x, y

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

def test_logcombine_issue():
    expr = logcombine(log(3) - log(2))
    # Assertion to check if the logcombine simplification is working as expected
    try:
        assert expr == log(3/2), "logcombine(log(3) - log(2)) did not return log(3/2)"
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exiting with status 1 to indicate the presence of the issue

if __name__ == "__main__":
    test_logcombine_issue()
    print("No issues detected.")  # This line executes if the above assertion passes
    sys.exit(0)
