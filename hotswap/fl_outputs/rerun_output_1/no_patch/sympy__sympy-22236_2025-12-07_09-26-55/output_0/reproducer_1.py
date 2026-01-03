from sympy import Mul, Rational, symbols
from sympy.printing.str import sstr
import traceback
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

x, y = symbols('x y')

mul1 = Mul(Rational(1, 2), x + y, evaluate=False)
mul2 = Mul(x + y, Rational(1, 2), evaluate=False)

expected_str1 = "(\\frac{1}{2})*(x + y)"
expected_str2 = "x + y*(\\frac{1}{2})"

actual_str1 = sstr(mul1)
actual_str2 = sstr(mul2)

assert actual_str1 == expected_str1, "The first Mul should be printed with brackets"
assert actual_str2 == expected_str2, "The second Mul should be printed with brackets"

print("No issues found")
