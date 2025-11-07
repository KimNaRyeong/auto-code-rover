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

def check_issue():
    from sympy import Rational, Pow, latex

    try:
        test_expr = latex(Pow(Rational(1, 2), -1, evaluate=False))
        assert test_expr is not None, "Expected a latex expression, got None"
    except RecursionError as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced: RecursionError occurred")

if __name__ == "__main__":
    check_issue()
    print("Issue not reproduced. Exiting with code 0.")
