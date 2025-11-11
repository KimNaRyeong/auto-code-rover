import sympy as sp

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

def reproduce_bug():
    try:
        x, y = sp.symbols('x y')
        expr1 = -2*sp.sympify('x') - 4*sp.sympify('y') - 8
        expr2 = expr1.extract_multiplicatively(-2)
        assert expr2 == 1 + 2*sp.I, "Expected 1 + 2*I but got {}".format(expr2)
    except AssertionError as e:
        print_stacktrace(e)
        raise

reproduce_bug()
