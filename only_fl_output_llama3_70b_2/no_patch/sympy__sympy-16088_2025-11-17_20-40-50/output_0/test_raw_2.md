Here is the revised `reproducer.py` file:
```
from sympy import symbols, Sum, Integral

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

x, y, n = symbols('x y n')

sum_expr = Sum(x*y, (x, 1, n))
int_expr = Integral(x*y, (x, 1, n))

sum_simplified = sum_expr.simplify()
int_simplified = int_expr.simplify()

try:
    assert str(sum_simplified) == str(n*y)
    assert not str(int_simplified).startswith('Integral')
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue is fixed!")
exit(0)
```
This script creates a sum expression and an integral expression, simplifies them, and then checks if the simplified expressions match the expected results. If they don't, it raises an `AssertionError` with a detailed stack trace.

Please try running this revised script to reproduce the issue.