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
except Exception as e:
    print_stacktrace(e)
else:
    print("The issue is fixed.")
```
When executed, this script will raise an `AssertionError` if the issue is present and print a stack trace. If the issue is fixed, it will print "The issue is fixed."

To execute the script, save it as `reproducer.py` in the root directory of the Sympy project and run `python3 reproducer.py`.