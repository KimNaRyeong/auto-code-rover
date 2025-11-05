import sympy as sp
from sympy import Symbol, fps
from functools import wraps

def assert_raises(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
            raise AssertionError("Expected an exception")
        except Exception as e:
            print_stacktrace(e)
            exit(0)
    return wrapper

@assert_raises
def reproduce_issue():
    x = Symbol('x')
    p = fps(x ** 2)

if __name__ == "__main__":
    reproduce_issue()
