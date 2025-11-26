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
This script creates an integral expression `Integral(x*y, (x, 1, n))` and simplifies it using the `simplify()` method. It then checks if the simplified expression has both `x` and `y` as factors. If not, it raises an `AssertionError`, prints a stack trace using the provided `print_stacktrace()` function, and exits with code 1.

If the issue is fixed, the simplified expression will correctly pull out the constant term, and the assertion will pass. The script then prints "Issue is fixed!" and exits with code 0.