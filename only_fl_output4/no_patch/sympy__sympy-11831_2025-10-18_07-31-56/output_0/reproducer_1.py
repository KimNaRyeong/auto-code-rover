# reproducer.py
import sympy as sp
from sympy import S, symbols, sets

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

def test_set_intersection():
    try:
        d = symbols("d")
        solution = sets.FiniteSet((d + 1, -d + 4, -d + 5, d))
        # This line attempts the intersection operation, which is expected to fail
        solution.intersect(S.Naturals0**4)
    except TypeError as e:
        if "object of type 'Naturals0' has no len()" in str(e):
            # Error message matches the issue, printing stack trace and asserting
            print_stacktrace(e)
            raise AssertionError("Issue reproduced successfully.") from e

    # If no exception is caught, or if a different error occurs, the issue might have been fixed or changed.
    print("Issue seems to be fixed or changed. Exiting with code 0.")
    exit(0)

if __name__ == "__main__":
    test_set_intersection()
