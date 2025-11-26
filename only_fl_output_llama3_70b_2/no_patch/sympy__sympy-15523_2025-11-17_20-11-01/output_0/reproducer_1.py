import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
from sympy.core.cache import cacheit
from functools import wraps

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def cache_wrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return cacheit(wrapper)

@cache_wrapper
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

try:
    case = "2!"
    transformations2 = {"implicit_multiplication_application": True}
    implicit = parse_expr(case, transformations=transformations2)
    assert isinstance(implicit, sp.Expr)
    
    raises(SympifyError, lambda: sp.sympify('lambda'))
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue is present")
else:
    print("No issue found")
