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
