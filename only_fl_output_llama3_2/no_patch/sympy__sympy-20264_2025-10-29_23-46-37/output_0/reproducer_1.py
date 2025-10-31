import sympy as sp
from sympy import Rational, Pow
from sympy.printing.latex import LatexPrinter

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

def reproduce_issue():
    try:
        latex_printer = LatexPrinter()
        latex_expr = latex_printer.doprint(Pow(Rational(1,2),-1, evaluate=False))
        print(latex_expr)
    except RecursionError as e:
        print_stacktrace(e)
        assert False, "Issue should be fixed"

if __name__ == "__main__":
    reproduce_issue()
