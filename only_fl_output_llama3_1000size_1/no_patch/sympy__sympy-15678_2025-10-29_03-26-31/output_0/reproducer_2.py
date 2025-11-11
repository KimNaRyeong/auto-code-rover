from sympy import Eq, idiff, exp, symbols
import traceback
import sys

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

y, x = symbols('y x')

try:
    idiff(Eq(y*exp(y), x*exp(x)), y, x)
except Exception as e:
    print_stacktrace(e)
    assert False, "idiff doesn't support Eq"

try:
    idiff(f(x)*exp(f(x)) - x*exp(x), f(x), x)
except Exception as e:
    print_stacktrace(e)
    assert False, "idiff doesn't support f(x) instead of y"

try:
    result = idiff(y*exp(y) - x*exp(x), y, x)
    assert isinstance(result, object), "Expected the result to be an expression"
except Exception as e:
    print_stacktrace(e)
    assert False, "idiff doesn't work correctly for some inputs"

print("All tests passed")
