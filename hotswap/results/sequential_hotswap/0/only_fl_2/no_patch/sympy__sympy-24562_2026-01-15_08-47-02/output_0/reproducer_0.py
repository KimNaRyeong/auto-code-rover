# reproducer.py
from sympy import Rational
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

def test_rational_calc():
    try:
        # The commands which are expected to show an incorrect behavior
        incorrect_behavior = Rational('0.5', '100')
        correct_behavior = Rational(0.5, 100)

        # Asserting the equivalence of both methods
        assert incorrect_behavior == correct_behavior, "Rational calculation mismatch"

    except AssertionError as e:
        print_stacktrace(e)
        raise e from None  # Raise the AssertionError to indicate a failure
    
    # If no AssertionError, the calculations are considered equivalent (issue is fixed)
    print("No issues, calculations match as expected.")

if __name__ == "__main__":
    test_rational_calc()
