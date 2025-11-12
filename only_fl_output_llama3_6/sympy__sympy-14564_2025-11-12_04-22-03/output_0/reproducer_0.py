import sympy as sp
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

def reproduce_issue():
    c = sp.ConditionSet(x, x > 5, sp.Interval(1, 7))
    try:
        result = c.subs(x, 8)
        assert isinstance(result, sp.EmptySet), "Expected EmptySet"
    except Exception as e:
        print_stacktrace(e)
        raise

def main():
    reproduce_issue()

if __name__ == "__main__":
    main()
