import sympy as sp
from sympy import Symbol, fps
from functools import wraps

def assert_raises(expected_exception):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except expected_exception as e:
                print_stacktrace(e)
                raise AssertionError("Expected exception not raised")
            else:
                raise AssertionError("Expected exception not raised")
        return wrapper
    return decorator

@assert_raises(TypeError)
def reproduce_issue():
    x = sp.Symbol('x')
    p = fps(x ** 2)

if __name__ == "__main__":
    reproduce_issue()
