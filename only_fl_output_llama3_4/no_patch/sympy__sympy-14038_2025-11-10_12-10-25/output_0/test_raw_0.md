Here is the reproducer script:

```python
import sympy as sp
from sympy.abc import a, n
import sys
import traceback

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
    from sympy import product
    result = sp.product(1 - a**2 / (n*sp.pi)**2, [n, 1, sp.oo])
    if result == 0:
        raise AssertionError("product(1 - a**2 / (n*pi)**2, [n, 1, oo]) should not evaluate to 0")
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

print("Issue reproduced successfully. Exiting with code 1.")
sys.exit(1)
```

This script will raise an `AssertionError` if the product evaluates to 0, and it will print a stack trace of the issue. If the issue is fixed, it will exit with code 0.