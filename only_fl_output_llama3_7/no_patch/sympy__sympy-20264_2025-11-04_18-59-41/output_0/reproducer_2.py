import sympy as sp
from sympy import Rational, Pow

def reproduce_issue():
    try:
        latex_expr = Pow(Rational(1, 2), -1, evaluate=False)
        print(latex_expr)
        assert latex_expr == "1^{-1}"  # This assertion will fail if the issue is present
    except RecursionError as e:
        print_stacktrace(e)

reproduce_issue()
