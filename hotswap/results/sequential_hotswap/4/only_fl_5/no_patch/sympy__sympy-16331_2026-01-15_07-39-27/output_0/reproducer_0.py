import sympy as sp
from sympy.utilities.autowrap import ufuncify
from sympy.abc import x, y

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', line_number, ":", code_context, file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    try:
        expr = x + y
        f = ufuncify((x, y), expr, backend='Cython')
        # If we reach this point without an exception, the issue is assumed to be fixed.
        print("Issue seems to be fixed")
    except Exception as e:
        print_stacktrace(e)
        assert False, "The issue is still present"

if __name__ == "__main__":
    main()
