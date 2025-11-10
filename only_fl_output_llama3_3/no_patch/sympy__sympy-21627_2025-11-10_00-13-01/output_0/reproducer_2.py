import sympy as sp

def reproduce_bug():
    expr = sp.sympify("cosh(acos(-i + acosh(-g + i)))")
    try:
        _ = expr.is_zero
    except RecursionError as e:
        print_stacktrace(e)
        raise AssertionError("Expected maximum recursion depth exceeded")

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

if __name__ == "__main__":
    try:
        reproduce_bug()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Bug not reproduced. Exiting with code 0.")
        exit(0)
