I apologize for the mistake. Here is a revised `reproducer.py` file that should reproduce the issue:
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

expr_sum = Sum(x*y, (x, 1, n))
expr_integral = Integral(x*y, (x, 1, n))

sum_simplified = expr_sum.simplify()
integral_simplified = expr_integral.simplify()

try:
    assert sum_simplified.args[0].is_Mul and integral_simplified.has(Integral)
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue is fixed!")
exit(0)
```
This script creates both a `Sum` expression and an `Integral` expression, simplifies them using the `simplify()` method, and then checks if the simplified `Sum` expression has a `Mul` factor (i.e., the constant term was pulled out) and if the simplified `Integral` expression still contains an `Integral` (i.e., the constant term was not pulled out). If either of these conditions is not met, it raises an `AssertionError`, prints a stack trace using the provided `print_stacktrace()` function, and exits with code 1.

If the issue is fixed, both assertions will pass, the script will print "Issue is fixed!" and exit with code 0.