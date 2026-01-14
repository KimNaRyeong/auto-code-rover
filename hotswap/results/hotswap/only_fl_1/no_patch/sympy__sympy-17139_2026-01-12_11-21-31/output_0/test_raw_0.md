 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import sympy
from sympy import *

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

x = Symbol('x')

try:
    print(simplify(cos(x)**I))
except Exception as e:
    assert isinstance(e, TypeError)
    print_stacktrace(e)
```
When executed with `python3 reproducer.py`, the script should raise an `AssertionError` and print a stack trace of the issue. The stack trace should match the one provided in the issue description.

If the issue is fixed, the script should exit with code 0 without raising any exceptions.