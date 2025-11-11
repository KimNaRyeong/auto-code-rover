Here is the reproducer script:

```python
import sympy as sp
from io import StringIO
from contextlib import redirect_stdout

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
    try:
        f = StringIO()
        with redirect_stdout(f):
            sp.printing.use_format("latex")
            result1 = str(sp.Mul(1/2, sp.sympify('x + y'), evaluate=False))
            result2 = str(sp.Mul(sp.sympify('x + y'), 1/2, evaluate=False))
        if "⋅" in f.getvalue():
            raise AssertionError("Issue not fixed")
    except Exception as e:
        print_stacktrace(e)
        exit(0)

if __name__ == "__main__":
    reproduce_issue()
```

This script will run the given code and check if the issue is present. If the issue is present, it will print the stack trace and exit with code 0.