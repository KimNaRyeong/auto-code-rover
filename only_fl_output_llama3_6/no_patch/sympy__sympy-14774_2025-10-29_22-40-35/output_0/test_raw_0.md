Here is the reproducer script:

```python
import sympy as sp
from sympy import latex, pi, sin, csc
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
        with StringIO() as f, redirect_stdout(f):
            print(latex(csc(pi/2), inv_trig_style="full"))
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    reproduce_issue()
```

This script will attempt to print the LaTeX representation of `csc(pi/2)` with full inverse trig function names. If the issue is present, it should raise an exception and print a stack trace.