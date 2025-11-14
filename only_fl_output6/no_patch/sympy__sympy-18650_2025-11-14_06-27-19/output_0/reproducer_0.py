# reproducer.py

from sympy import sqrt, Rational

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

def test_sqrt_rational():
    result = sqrt(8)**Rational(2, 3)
    expected = 2
    try:
        assert result == expected, f"Expected {expected}, got {result}"
    except AssertionError as e:
        print_stacktrace(e)
        raise e

if __name__ == "__main__":
    try:
        test_sqrt_rational()
    except AssertionError:
        exit(1)
    exit(0)
