Here is the reproducer script:

```python
import sympy as sp
from sympy import *

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

def reproduce_issue():
    x, y = symbols('x y')
    try:
        expand_trig(csch(x + y))
        expand_trig(sech(x + y))
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    reproduce_issue()
```

This script will attempt to expand the `csch` and `sech` functions using the `expand_trig` function. If an exception is raised, it will print the stack trace and then re-raise the exception.