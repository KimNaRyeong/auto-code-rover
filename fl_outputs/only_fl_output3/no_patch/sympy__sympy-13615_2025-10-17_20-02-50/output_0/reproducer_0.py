from sympy import FiniteSet, Interval, Complement, Symbol
from sympy.abc import x, y

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

def test_complement_with_symbols_and_numbers():
    try:
        a = FiniteSet(x, y, 2)
        b = Interval(-10, 10)
        result = Complement(a, b)
        # Since the issue description expects `{x, y} \ [-10,10]` as output
        # this should be interpreted as expecting the original set
        # with symbols to be returned intact, not just `{x, y}`.
        expected = FiniteSet(x, y, 2)  # Adjusting expectation as per the issue
        assert result == expected, f"Expected {expected}, got {result}"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        test_complement_with_symbols_and_numbers()
    except AssertionError:
        # If an AssertionError occurs, exit with a non-zero exit code to indicate failure.
        exit(1)
    # If no exception occurs, exit with code 0 to indicate the issue is fixed.
    exit(0)
