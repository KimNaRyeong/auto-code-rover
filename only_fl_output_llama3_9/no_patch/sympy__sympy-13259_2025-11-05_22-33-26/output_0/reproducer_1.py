import sympy as sp
from sympy import I, cos, pi, sqrt, asinh

def main():
    a = 2*sp.sqrt(2)*I*sp.cos(pi/6 - I*asinh(5*sp.sqrt(2)/2)/3)/3
    b = a.simplify()
    
    if not sp.N(b).evalf() == sp.N(a).evalf():
        raise AssertionError("Simplification failed")
    else:
        print("Issue fixed")

try:
    main()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
