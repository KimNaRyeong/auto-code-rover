Here is the `reproducer.py` file that reproduces the issue:

```python
import sympy as sp
from sympy.abc import x

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    assert str(x*sp.Poly(1)) != "Poly(x, x, domain='ZZ')"
    raise AssertionError("Issue not reproduced")

except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue fixed")
exit(0)
```

This script will run the expression `x*Poly(1)` and check if it produces the expected result. If the assertion fails, it will print the stack trace and exit with code 1. Otherwise, it will print a success message and exit with code 0.

Please note that this reproducer is specific to your issue and may not work for other issues.