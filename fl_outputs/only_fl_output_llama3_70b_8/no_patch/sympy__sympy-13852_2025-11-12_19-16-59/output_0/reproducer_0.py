import sympy as sp
from sympy.functions import polylog, exp_polar

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
    result = sp.polylog(2, sp.Rational(1, 2)).expand(func=True)
    try:
        assert sp.nsimplify(result.evalf(), [sp.pi**2, sp.log(2)**2]) == expected_result
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)

def test_polylog_derivative():
    z = sp.symbols('z')
    result = sp.diff(sp.polylog(1, z) - sp.expand_func(sp.polylog(1, z)), z)
    try:
        assert result == 0
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)

if __name__ == "__main__":
    test_polylog_expansion()
    test_polylog_derivative()
