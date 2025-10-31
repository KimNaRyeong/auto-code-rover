import sympy as sp
from sympy.abc import z, pi
from sympy.functions.elementary.miscellaneous import Rational

def reproduce_issue():
    try:
        expanded = sp.expand_func(sp.polylog(1, Rational(1, 2)))
        assert str(expanded) == "-log(z*exp_polar(-I*pi) + 1)"
    except AssertionError as e:
        print_stacktrace(e)
        raise
    else:
        exit(0)

if __name__ == "__main__":
    reproduce_issue()
