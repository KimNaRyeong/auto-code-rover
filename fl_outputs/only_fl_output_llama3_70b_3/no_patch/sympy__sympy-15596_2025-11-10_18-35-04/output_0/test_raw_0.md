Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
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

x = sp.symbols('x')
f = (x-2)/(x**2+1)

try:
    assert degree(f, x) != 1
except AssertionError as e:
    print_stacktrace(e)
    raise SystemExit(1)

print("Issue is fixed!")
```
This script defines the rational function `f` and tries to compute its degree using `degree(f, x)`. If the result is `1`, which is the incorrect behavior, it raises an `AssertionError` with a stack trace. If the issue is fixed, it prints "Issue is fixed!" and exits with code 0.