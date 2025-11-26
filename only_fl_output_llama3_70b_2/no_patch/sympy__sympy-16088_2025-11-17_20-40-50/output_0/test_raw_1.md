Here is the `reproducer.py` file:
```
from sympy import symbols, Integral

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

expr = Integral(x*y, (x, 1, n))
simplified_expr = expr.simplify()

try:
    assert simplified_expr.args[0].has(x) and simplified_expr.args[0].has(y)
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue is fixed!")
exit(0)
```
This script defines the symbols `x`, `y`, and `n` using SymPy. It then creates an integral expression `Integral(x*y, (x, 1, n))` and attempts to simplify it using the `simplify()` method.

The script checks if the simplified expression has both `x` and `y` as factors. If not, it raises an `AssertionError`. The `print_stacktrace()` function is used to print a detailed stack trace of the error, including line numbers and code context.

If the issue is fixed, the script will simply print "Issue is fixed!" and exit with code 0.