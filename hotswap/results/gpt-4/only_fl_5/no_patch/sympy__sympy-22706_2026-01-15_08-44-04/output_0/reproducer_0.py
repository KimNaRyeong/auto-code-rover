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

def reproduce_issue():
    from sympy import symbols, Mul, Pow

    x = symbols('x')
    try:
        expr = Mul(Pow(x,-2, evaluate=False), Pow(3,-1,evaluate=False), evaluate=False)
        print(expr)
    except IndexError as e:
        print_stacktrace(e)
        raise AssertionError("The issue is present.") from e

    # If no exception was raised, assume the issue is fixed.
    print("No issue detected, the issue might have been fixed.")

if __name__ == "__main__":
    reproduce_issue()
