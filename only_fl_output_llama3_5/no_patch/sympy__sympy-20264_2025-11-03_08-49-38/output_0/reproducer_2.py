import sympy as sp
from sympy import Rational, Pow

def reproduce_issue():
    try:
        latex_expr = Pow(Rational(1, 2), -1, evaluate=False)
        print(latex_expr)
        assert Pow(Rational(1, 3), -1, evaluate=False) == '1^{-1}'
        raise AssertionError("Expected Pow(Rational(1, 3), -1, evaluate=False) to equal '1^{-1}'")
    except RecursionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    reproduce_issue()
