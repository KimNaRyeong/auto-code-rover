import sympy as sp
from sympy.functions import polylog, exp_polar
from sympy.simplify import nsimplify

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

def test_polylog_expansion():
    z = sp.symbols('z')
    expected_result = -sp.log(2)**2/2 + sp.pi**2/12
    result = nsimplify(sp.expand_func(polylog(2, 1/sp.Rational(1,2))).evalf(), [sp.pi**2, sp.log(2)**2])
    if result != expected_result:
        raise AssertionError(f"Expected {expected_result} but got {result}")

def test_polylog_derivative():
    z = sp.symbols('z')
    polylog_expr = polylog(1, z)
    expanded_expr = sp.expand_func(polylog_expr)
    derivative = sp.diff(polylog_expr - expanded_expr, z)
    if derivative != 0:
        raise AssertionError(f"Expected derivative to be 0 but got {derivative}")

if __name__ == "__main__":
    try:
        test_polylog_expansion()
        test_polylog_derivative()
    except Exception as e:
        print_stacktrace(e)
        exit(1)
