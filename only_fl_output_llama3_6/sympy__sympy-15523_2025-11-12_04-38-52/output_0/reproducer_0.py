import sympy as sp
from sympy.parsing.sympy_parser import parse_expr

def test_reproducer():
    try:
        implicit = parse_expr('factorial()')
        raise AssertionError("Expected TypeError: factorial takes exactly 1 argument (0 given)")
    except TypeError as e:
        print_stacktrace(e)

try:
    sp.sympify('lambda x: x**2')
    raise AssertionError("Expected SympifyError")
except TypeError as e:
    print_stacktrace(e)
