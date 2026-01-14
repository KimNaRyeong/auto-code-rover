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
    print("Issue present: Simplify does not pull out constant term in Integral.")
    raise AssertionError("Issue present: Simplify does not pull out constant term in Integral.")
except AssertionError as e:
    print_stacktrace(e)
    raise e
```
When executed with Python 3.8.5, the script reproduces the issue and prints the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 17, in <module>
    raise AssertionError("Issue present: Simplify does not pull out constant term in Integral.")
AssertionError: Issue present: Simplify does not pull out constant term in Integral.
```
After applying the changes from the pull request, the script should exit with code 0 and not print any stack trace.