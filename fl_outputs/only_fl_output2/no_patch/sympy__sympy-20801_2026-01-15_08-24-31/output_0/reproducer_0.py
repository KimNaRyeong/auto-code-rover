from sympy import *
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

def test_sym_comparison():
    try:
        # Testing the comparison from the issue both ways
        assert S(0.0) == S.false, "S(0.0) should equal S.false"
        assert S.false == S(0.0), "S.false should equal S(0.0)"

        # Additionally testing comparison to S(0) for consistency
        assert S(0) == S.false == False, "S(0) should not equal S.false and both should evaluate to False"

        print("Test passed: Issue is fixed.")
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with a non-zero code to indicate a failure

if __name__ == "__main__":
    test_sym_comparison()
    sys.exit(0)  # Exit with 0 when the issue is fixed or no issue is present
