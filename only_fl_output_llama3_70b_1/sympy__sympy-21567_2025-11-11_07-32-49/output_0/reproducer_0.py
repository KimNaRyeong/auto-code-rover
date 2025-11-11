import sympy as sp
from sympy import symbols, tanh, csch, sech, csc, sec

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
    assert sp.expand_trig(tanh(x + y)) == (sp.tanh(x) + sp.tanh(y))/(sp.tanh(x)*sp.tanh(y) + 1)
    assert sp.expand_trig(csc(x + y)) == 1/(sp.sin(x)*sp.cos(y) + sp.sin(y)*sp.cos(x))
    assert sp.expand_trig(sec(x + y)) == 1/(-sp.sin(x)*sp.sin(y) + sp.cos(x)*sp.cos(y))
    assert sp.expand_trig(csch(x + y)) != csch(x + y)
    assert sp.expand_trig(sech(x + y)) != sech(x + y)
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue is fixed!")
exit(0)
