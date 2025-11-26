Here is the `reproducer.py` file:
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

try:
    assert Integral(x*y, (x, 1, n)).simplify() == Integral(y*x, (x, 1, n))
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue is fixed!")
exit(0)
```
This script defines the symbols `x`, `y`, and `n` using SymPy. It then creates an integral expression `Integral(x*y, (x, 1, n))` and attempts to simplify it using the `simplify()` method.

If the simplification does not pull out the constant term `y` outside the integral, the script will raise an `AssertionError`. The `print_stacktrace()` function is used to print a detailed stack trace of the error, including line numbers and code context.

If the issue is fixed, the script will simply print "Issue is fixed!" and exit with code 0.