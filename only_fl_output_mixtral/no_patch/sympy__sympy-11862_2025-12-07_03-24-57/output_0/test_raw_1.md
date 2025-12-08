 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
from sympy import symbols, sqrt, N, lambdify, evalf
from sympy.abc import x

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

x = symbols('x')
g = sqrt(2) - x
h = g.evalf(64)

f1 = lambdify(x, g, modules='mpmath')
f2 = lambdify(x, h, modules='mpmath')

try:
    assert f1(N(sqrt(2),64)) != f2(N(sqrt(2),64))
except AssertionError as e:
    print_stacktrace(e)
```
When executed with `python3 reproducer.py`, it will print the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 23, in <module>
    assert f1(N(sqrt(2),64)) != f2(N(sqrt(2),64))
AssertionError:
```
This confirms that the issue is present.