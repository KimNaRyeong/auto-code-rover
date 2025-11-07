import sympy as sp
from functools import wraps

def assert_raises(expected_exception, func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
            raise AssertionError("Expected an exception but got nothing")
        except expected_exception:
            pass
    return wrapper

@assert_raises(AssertionError)
def reproducer():
    J = sp.symbols('J')
    j = sp.symbols('j')
    second = sp.symbols('s**2')
    
    result = sp.convert_to(J * j * second, J)
    print_stacktrace(result)

if __name__ == "__main__":
    try:
        reproducer()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Issue is fixed")
        exit(0)
