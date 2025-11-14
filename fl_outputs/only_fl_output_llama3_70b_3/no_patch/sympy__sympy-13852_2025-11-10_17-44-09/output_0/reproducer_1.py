import sympy as sp
from sympy.functions import polylog

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
    result = polylog(1, z).expand(func=True)
    expected_result = -sp.log(1-z)
    try:
        assert result == expected_result
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)

def test_polylog_derivative():
    z = sp.symbols('z')
    result = polylog(1, z).expand(func=True)
    derivative = sp.diff(result, z)
    expected_derivative = z/(1-z)
    try:
        assert derivative == expected_derivative
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)

if __name__ == "__main__":
    test_polylog_expansion()
    test_polylog_derivative()
