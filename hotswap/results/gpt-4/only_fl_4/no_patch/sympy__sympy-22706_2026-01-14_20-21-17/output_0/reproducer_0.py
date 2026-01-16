# reproducer.py

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

def test_issue():
    from sympy import Mul, Pow, Symbol

    x = Symbol('x')
    try:
        print(Mul(Pow(x, -2, evaluate=False), Pow(3, -1, evaluate=False), evaluate=False))
    except IndexError as e:
        print_stacktrace(e)
        raise AssertionError("IndexError is present") from e

    # If there's no exception, assume the issue has been resolved
    print("No issue detected.")

if __name__ == "__main__":
    test_issue()
