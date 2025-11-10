Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import sympy

def test_rootof_issue():
    x = sympy.symbols('x')
    t = sympy.symbols('t')

    # Test 1
    rootof_expr1 = sympy.RootOf(x**3 + x - 1, 0)
    assert rootof_expr1.poly.gen == x

    # Test 2
    expr2 = (x**3 + x - 1).subs(x, sympy.tan(x))
    rootof_expr2 = sympy.RootOf(expr2, 0)
    try:
        assert rootof_expr2.poly.gen == sympy.tan(x)
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)

    # Test 3
    expr3 = tan(x)**3 + 2*tan(x) - 1
    rootof_expr3 = sympy.RootOf(expr3, 0)
    assert rootof_expr3.poly.gen == sympy.tan(x)

    # Test 4
    expr4 = x**3 + 2*x - 1
    rootof_expr4 = sympy.RootOf(expr4, 0)
    try:
        assert rootof_expr4.poly.gen != sympy.tan(x)
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)

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

if __name__ == "__main__":
    test_rootof_issue()
```
This script will raise an `AssertionError` and print a stack trace when the issue is present, and exit with code 0 when the issue is fixed.