# reproducer.py
from sympy import Symbol, Pow, Mul

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

def test_sympy_issue():
    a = Symbol('a')
    u = Symbol('u')

    a2inv = Pow(Mul(a, a, evaluate=False), -1, evaluate=False)
    d = Mul(-2, u, a2inv, evaluate=False)

    expected_output = "-2*u/(a*a)"
    actual_output = str(d)

    try:
        assert actual_output == expected_output, "The output does not match the expected format for multiplication."
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        test_sympy_issue()
    except AssertionError:
        # Exit with non-zero code when an AssertionError is raised
        import sys
        sys.exit(1)
    # Exit with code 0 when the issue is fixed.
    print("Issue fixed.")
    sys.exit(0)
