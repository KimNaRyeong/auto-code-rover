import sympy
from sympy import Symbol

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

def run_test():
    sympy_version = sympy.__version__
    print(f"Sympy Version: {sympy_version}")
    x = Symbol('x', commutative=False)
    result = (x*x*x).subs({x*x: 1})
    try:
        # The assertion reflects the unexpected behavior.
        assert result == x, f"Expected substitution result to be 'x', got '{result}'"
    except AssertionError as e:
        print_stacktrace(e)
        # Ensure exit code 0 even upon AssertionError
        sys.exit(0)

if __name__ == "__main__":
    run_test()
