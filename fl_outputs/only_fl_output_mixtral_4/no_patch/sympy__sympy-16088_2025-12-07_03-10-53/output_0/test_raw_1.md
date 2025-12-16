 Here is a standalone Python script that reproduces the issue:
```python
from sympy import Integral, Sum, simplify
from sympy.abc import x, y, z, n

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

# Reproduce the issue
try:
    integral = Integral(x*y, (x, 1, n))
    simplified_integral = simplify(integral)
    assert simplified_integral != integral.doit()
    print("Issue present: Simplify does not pull out the constant term in Integral.")
    raise AssertionError("Simplify does not pull out the constant term in Integral.")
except AssertionError as e:
    print_stacktrace(e)
```
When executed, the script should print:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 18, in <module>
    raise AssertionError("Simplify does not pull out the constant term in Integral.")
AssertionError: Simplify does not pull out the constant term in Integral.
```
After the fix is applied, the script should not print anything and exit with code 0.