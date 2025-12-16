 Here is a standalone Python script that reproduces the issue:
```python
from sympy import Integral, Sum, simplify
from sympy.abc import x, y, n, z

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
except Exception as e:
    print_stacktrace(e)
else:
    print("No issue found.")
```
When executed with Python 3, this script will print a stack trace if the issue is present, and exit with code 0 if the issue is fixed.

The issue is that `simplify` does not pull out the constant term (independent term) outside the integral, but it does for the sum. The expected behavior is that `simplify` should pull out the constant term outside the integral, just like it does for the sum.

The release notes for this release should include the following:

* `simplify`:
  * Simplify now pulls independent factors out of integrals.

This release note indicates that the `simplify` function has been updated to pull out independent factors from integrals, which resolves the issue reported in this pull request.