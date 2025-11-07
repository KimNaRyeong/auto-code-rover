import sympy as sp
from sympy import *
import traceback
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    from sympy import *
    x, y = symbols('x y')
    assert expand_trig(csch(x + y)) != csch(x + y), "Expected csch to be expanded"
    assert expand_trig(sech(x + y)) != sech(x + y), "Expected sech to be expanded"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
else:
    print("Test passed")
    exit(0)
