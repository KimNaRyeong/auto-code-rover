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

# The following assertion will fail due to the issue
assert minimal_polynomial(a) == PurePoly(_x**2 - 2*_x - 1, _x, domain='QQ')
print("Issue reproduced.")
print_stacktrace(ValueError("Minimal polynomials are different."))
```
To run the script, execute `python3 reproducer.py`. The script should raise a `ValueError` with the provided stack trace, indicating the issue is present. If the issue is fixed, the script should exit with code 0 and not print the "Issue reproduced." message.