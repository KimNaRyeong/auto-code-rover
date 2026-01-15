# reproducer.py
from sympy import sqrt, Rational

def assert_issue():
    # Attempting to reproduce the issue where sqrt(8)**Rational(2, 3) doesn't simplify to 2
    result = sqrt(8)**Rational(2, 3)
    expected = 2
    # Asserting the simplification equals 2, to confirm the issue. 
    assert result == expected, f"Expected {expected}, got {result}"

if __name__ == "__main__":
    try:
        assert_issue()
    except AssertionError as e:
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
        
        print_stacktrace(e)
        raise SystemExit(1)  # Indicate failure by non-zero exit
    else:
        print("No issues detected.")
