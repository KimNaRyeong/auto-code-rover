# reproducer.py
import sympy

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

def main():
    sympy_version = sympy.__version__
    print(f"Using sympy version: {sympy_version}")
    x = sympy.Symbol('x', commutative=False)
    try:
        result = (x*x*x).subs({x*x: 1})   # The substitution should not simplify to 1 for noncommutative symbols
        # We expect the substitution not to simplify to 1, thereby expecting `x`
        assert result != 1, f"Unexpected simplification result: {result}. Expected something different from 1."
        print("Test passed: The issue appears to be fixed.")
    except AssertionError as ae:
        print_stacktrace(ae)
        raise ae

if __name__ == "__main__":
    try:
        main()
    except AssertionError:
        exit(1)
    exit(0)
