import sympy as sp
from sympy import I, Integer

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

def reproduce_issue():
    S1 = sp.imageset(lambda n: n + (n - 1) * (n + 1) * I, sp.S.Integers)
    assert not (2 in S1), "Issue #19513"
    assert not (2 in S1.intersect(sp.Reals)), "Issue #19513"

try:
    reproduce_issue()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue fixed")
exit(0)
