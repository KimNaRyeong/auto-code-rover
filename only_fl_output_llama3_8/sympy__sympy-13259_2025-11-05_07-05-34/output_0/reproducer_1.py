import sympy as sp
from sympy import I, sqrt, pi, cos, asinh

def main():
    a = 2*sqrt(2)*I*cos(pi/6 - I*asinh(5*sqrt(2)/2)/3)/3
    b = a.simplify()
    if not sp.Eq(a.evalf(), b.evalf()):
        raise AssertionError("Simplification failed")
    print("Issue reproduced successfully")

try:
    main()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
