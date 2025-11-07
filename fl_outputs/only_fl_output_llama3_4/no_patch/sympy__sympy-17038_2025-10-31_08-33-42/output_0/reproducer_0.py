import sympy
from sympy.core.power import isqrt

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
    try:
        n = 4503599761588224
        s = isqrt(n)
        assert s**2 <= n, "isqrt gives incorrect results"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    sympy.init_printing(use_unicode=True)  # Initialize SymPy printing
    reproduce_issue()
