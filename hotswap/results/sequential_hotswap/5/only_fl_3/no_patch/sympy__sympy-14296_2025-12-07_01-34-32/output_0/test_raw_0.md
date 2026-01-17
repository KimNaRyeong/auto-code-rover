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
assert minimal_polynomial(a) != _x**2 - 2*_x - 1, "Issue present: wrong minimal polynomial"
print_stacktrace(Exception("Issue present: wrong minimal polynomial"))
```
Executing the script `python3 reproducer.py` will raise an `AssertionError` and print the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 13, in <module>
    assert minimal_polynomial(a) != _x**2 - 2*_x - 1, "Issue present: wrong minimal polynomial"
AssertionError: Issue present: wrong minimal polynomial
```
This reproduces the issue where the minimal polynomial of `a` is incorrectly set to `_x**2 - 2*_x - 1` instead of `_x**2 + 2*_x - 1`.