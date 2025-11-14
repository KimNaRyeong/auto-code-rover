import sympy as sp

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

x, y = sp.symbols('x y')

try:
    assert sp.expand_trig(sp.csch(x + y)) != sp.csch(x + y), "csch is not expanded correctly"
    assert sp.expand_trig(sp.sech(x + y)) != sp.sech(x + y), "sech is not expanded correctly"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue is fixed")
exit(0)
