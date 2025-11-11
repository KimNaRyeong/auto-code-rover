Here is the reproducer script:

```python
import sympy as sp
from io import StringIO
from contextlib import redirect_stdout
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

def reproduce_issue():
    try:
        from sympy import *
        a = Symbol('a')
        u = Symbol('u')

        a2inv = Pow(Mul(a,a,evaluate=False), -1, evaluate=False)
        d = Mul(-2, u, a2inv, evaluate=False)

        f = StringIO()
        with redirect_stdout(f):
            print("This should be -2*u/(a*a)")
            print(d)

        output = f.getvalue().strip()

        if output != "This should be -2*u/(a*a)\n-2*u/a*a":
            raise AssertionError("Issue not reproduced")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

You can run this script with `python3 reproducer.py` to see the issue.