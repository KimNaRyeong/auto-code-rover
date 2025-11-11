import sympy as sp
from sympy.abc import x, y, n, z

def reproduce_issue():
    try:
        result = sp.Integral(x*y, (x, 1, n)).simplify()
        assert False, "Expected an error"
    except Exception as e:
        print_stacktrace(e)

if __name__ == "__main__":
    reproduce_issue()
