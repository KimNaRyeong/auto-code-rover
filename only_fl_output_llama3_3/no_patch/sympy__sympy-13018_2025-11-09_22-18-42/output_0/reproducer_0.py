import sympy
from sympy import Symbol, Pow
from functools import wraps

def assert_raises(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AssertionError as e:
            print_stacktrace(e)
            raise SystemExit(0)
    return wraps(func)(wrapper)

@assert_raises
def reproduce_issue():
    x = Symbol('x', commutative=False)
    result = (x*x*x).subs({x*x: 1})
    assert result == x, "Expected {} but got {}".format(x, result)

if __name__ == "__main__":
    reproduce_issue()
