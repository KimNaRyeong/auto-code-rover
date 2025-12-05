from sympy import *
from sympy.simplify.trigsimp import _futrig
from sympy.core.expr import Expr
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class MyExpr(Expr):
    def __init__(self, value):
        self.value = value

    def __pow__(self, other):
        return MyExpr(self.value ** other.as_complex())

    def __lt__(self, other):
        if not isinstance(other, MyExpr):
            return False
        return self.value < other.value

def _my_f(rv):
    if (rv.exp < 0) == True:
        return -rv.exp
    return rv

def test_simplify():
    x = Symbol('x')
    try:
        print(_futrig(MyExpr(1), _my_f, evaluate=False))
    except Exception as e:
        print_stacktrace(e)
        assert False

test_simplify()
print("The issue is present.")
