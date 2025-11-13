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

from sympy import *

def test_latex_conversion():
    expressions = [
        Pow(Rational(1, 2), -1, evaluate=False),
        Pow(Rational(-1, -5), -1, evaluate=False)
    ]

    for expr in expressions:
        try:
            latex_expr = latex(expr)
            print(f"Latex conversion successful: {latex_expr}")
        except RecursionError as e:
            print_stacktrace(e)
            assert False, "RecursionError occurred while converting to Latex"

if __name__ == "__main__":
    test_latex_conversion()
