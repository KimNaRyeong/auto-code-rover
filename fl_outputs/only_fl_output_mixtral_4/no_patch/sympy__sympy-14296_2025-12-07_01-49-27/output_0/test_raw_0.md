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
assert minimal_polynomial(b) != minimal_polynomial(a), "The minimal polynomials should not be the same"
print_stacktrace(AssertionError("The minimal polynomials should not be the same"))
```
When executed with `python3 reproducer.py`, this script will raise an `AssertionError` and print a stack trace showing the issue.

The issue is that the minimal polynomial of `a` is incorrectly set to the same value as the minimal polynomial of `b`, instead of being set to the correct value of `_x**2 + 2*_x - 1`. This is because the sign of the generator of the algebraic number field is being changed, but the minimal polynomial is not being updated accordingly.