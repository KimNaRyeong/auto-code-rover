import sympy as sp
from sympy import Mod, floor, Eq, And

def test_as_relational():
    x = sp.symbols('x')
    range_obj = sp.Range(3, 11, 2)
    relational_expr = range_obj.as_relational(x)
    if relational_expr != "(x >= 3) & (x <= 9) & Eq(x, floor(x))":
        print_stacktrace(AssertionError("Expected incorrect relational expression"))
    else:
        print("Test passed")

if __name__ == "__main__":
    test_as_relational()
