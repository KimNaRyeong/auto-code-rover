# reproducer.py
from sympy import *
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    x = MatrixSymbol('x', 2, 2)
    y = MatrixSymbol('y', 2, 2)
    expr = (x*y).subs(y, -y)
    expr_latex = latex(expr)
    # Expected that the output LaTeX shows parentheses around `-y`
    expected_latex_substr = 'x \\left(- y\\right)'

    if expected_latex_substr not in expr_latex:
        raise AssertionError(f"Expected to find '{expected_latex_substr}' in the LaTeX output '{expr_latex}' but didn't.")

try:
    main()
    print("Issue not present, program exits with code 0.")
    sys.exit(0)
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)
