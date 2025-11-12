import sympy as sm
from collections import Mapping, defaultdict
from collections.abc import Callable
from abc import ABC, abstractmethod

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

t, t0, tf = sm.symbols('t, t0, tf')
x = sm.Function('x')(t)
y = sm.Function('y')(t)
J = sm.Integral((x - y)**2, (t, t0, tf))
result = J.as_sum(20, 'trapezoid')

assert isinstance(result, sm.Sum), "Integral.as_sum() should output a Sum() object"

print_stacktrace(AssertionError("Integral.as_sum() should output a Sum() object"))
exit(1)
