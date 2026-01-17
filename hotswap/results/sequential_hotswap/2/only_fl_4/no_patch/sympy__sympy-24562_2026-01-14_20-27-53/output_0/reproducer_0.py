# reproducer.py
from sympy import Rational

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

def test_rational():
    try:
        # Creating a Rational object from string inputs
        rational_from_string = Rational('0.5', '100')
        # Creating a Rational object from numeric inputs
        rational_from_numbers = Rational(0.5, 100)
        
        # Assert that both ways of creating the Rational object should result in the same value
        assert rational_from_string == rational_from_numbers, "Mismatch in Rational values"

        # If the issue exists, the above assertion will fail, and the expected value is clarified here
        true_rational_value = Rational(1, 200)
        assert rational_from_numbers == true_rational_value, f"Rational value is not as expected, got {rational_from_numbers}"
    except AssertionError as e:
        print_stacktrace(e)
        raise  # Re-raise AssertionError to exit with non-zero (indicating failure/test-case not passed)

if __name__ == "__main__":
    try:
        test_rational()
    except AssertionError:
        exit(1)  # Exit with code 1 to indicate issue presence/failure
    exit(0)  # Exit with code 0 to indicate success/issue fixed
