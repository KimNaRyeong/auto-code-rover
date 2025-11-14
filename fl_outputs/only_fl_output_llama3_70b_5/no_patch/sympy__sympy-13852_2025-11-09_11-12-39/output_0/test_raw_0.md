Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import sympy as sp
from sympy.functions import polylog, exp_polar

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

z = sp.symbols('z')

try:
    assert sp.expand_func(polylog(2, 1/sp.Rational(2))).evalf() == -sp.log(2)**2/2 + sp.pi**2/12
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

try:
    assert sp.expand_func(polylog(1, z)).evalf(subs={z: 0.5}) == -sp.log(1 - 0.5)
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue is fixed!")
exit(0)
```
This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue. It will also exit with code 0 when the issue is fixed.