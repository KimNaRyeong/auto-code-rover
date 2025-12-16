 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
from sympy import sqrt, to_number_field, minimal_polynomial, PurePoly
from sympy.abc import _x

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

b = 1 - sqrt(2)
a = to_number_field(b)

if minimal_polynomial(a) != PurePoly(_x**2 + 2*_x - 1, _x, domain='QQ'):
    raise AssertionError("The minimal polynomial of `a` is not as expected.")
else:
    print("The minimal polynomial of `a` is as expected.")
```
When executed with `python3 reproducer.py`, this script will raise an `AssertionError` with a stack trace, reproducing the issue. The script will exit with a non-zero exit code.

When the issue is fixed, the script will print "The minimal polynomial of `a` is as expected." and exit with a zero exit code.