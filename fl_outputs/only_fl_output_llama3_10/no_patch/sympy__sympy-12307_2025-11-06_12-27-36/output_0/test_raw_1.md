Here is the reproducer script:

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
    import sympy as sp
    from sympy.abc import x
    if sp.fcode(sp.sign(x)) != '      sign(1, x)':
        raise AssertionError("Issue not fixed")
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue not fixed")
```

This script will attempt to generate Fortran code for the sign function using Sympy. If the generated code is not equal to "sign(1, x)", it will raise an `AssertionError` with the message "Issue not fixed" and print a stack trace of the issue.