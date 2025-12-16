from sympy import Mul, Rational, symbols, sstr
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
expected_str2 = "(x + y)*(\\frac{1}{2})"

actual_str1 = sstr(mul1)
actual_str2 = sstr(mul2)

if actual_str1 != expected_str1:
    raise AssertionError(f"Printing of unevaluated Mul needs brackets. Actual:\n{actual_str1}\nExpected:\n{expected_str1}")

if actual_str2 != expected_str2:
    raise AssertionError(f"Printing of unevaluated Mul needs brackets. Actual:\n{actual_str2}\nExpected:\n{expected_str2}")

print("No AssertionError raised. The issue is fixed.")
