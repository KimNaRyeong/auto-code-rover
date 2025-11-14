import sympy
from sympy import *

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

x, y = symbols('x y')

try:
    assert expand_trig(tanh(x + y)) == (tanh(x) + tanh(y))/(tanh(x)*tanh(y) + 1), "expand_trig for tanh is not correct"
    assert expand_trig(csc(x + y)) == 1/(sin(x)*cos(y) + sin(y)*cos(x)), "expand_trig for csc is not correct"
    assert expand_trig(sec(x + y)) == 1/(-sin(x)*sin(y) + cos(x)*cos(y)), "expand_trig for sec is not correct"
    assert expand_trig(csch(x + y)) != csch(x + y), "expand_trig for csch is not expanded correctly"
    assert expand_trig(sech(x + y)) != sech(x + y), "expand_trig for sech is not expanded correctly"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
