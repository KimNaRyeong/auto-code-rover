import sympy as sp
from sympy.abc import z, pi
from sympy.functions.elementary.miscellaneous import Rational

def reproduce_issue():
    try:
        result = sp.polylog(2, Rational(1, 2)).expand(func=True).evalf()
        expected_result = -sp.log(2)**2/2 + pi**2/12
        if not sp.simplify(result - expected_result) == 0:
            raise AssertionError("Expected result does not match")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
