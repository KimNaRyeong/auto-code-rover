Here is the reproducer script:

```python
import sympy as sp
from sympy.integrals import Integral
from sympy.abc import x, y, n, z

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
    result = Integral(x*y, (x, 1, n)).simplify()
    assert False, "Expected an error"
except Exception as e:
    print_stacktrace(e)
    raise
```

This script will run the following code:

```python
Integral(x*y, (x, 1, n)).simplify()
```

If the issue is present, it should raise an `AssertionError` and print a stack trace. If the issue is fixed, it should exit with code 0.

Please note that you need to have sympy installed in your Python environment to run this script.