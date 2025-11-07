# reproducer.py
from sympy import symbols, sets, S

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

def test_intersection_issue():
    try:
        d = symbols("d")
        solution = sets.FiniteSet((d + 1, -d + 4, -d + 5, d))
        _ = solution.intersect(S.Naturals0**4)
        # If the operation above does not raise an exception, the issue is considered resolved.
        print("The issue has been resolved.")
    except TypeError as e:
        print_stacktrace(e)
        raise AssertionError("The issue is present.") from e

if __name__ == "__main__":
    test_intersection_issue()
