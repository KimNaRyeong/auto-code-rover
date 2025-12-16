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
    assert simplified_integral != integral
except AssertionError:
    print("Issue reproduced: Simplify does not pull out constant term in Integral")
    raise
except Exception as e:
    print_stacktrace(e)

# Verify the fix
try:
    integral = Integral(x*y, (x, 1, n))
    simplified_integral = simplify(integral)
    assert simplified_integral == integral
except AssertionError:
    print("Issue not fixed: Simplify does not pull out constant term in Integral")
    raise
except Exception as e:
    print_stacktrace(e)
```
When executed with the previous version of Sympy, the script should raise an `AssertionError` and print a stack trace. When executed with the fixed version of Sympy, the script should not raise any exceptions and exit with code 0.