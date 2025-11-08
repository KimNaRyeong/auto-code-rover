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
    f = StringIO()
    with redirect_stdout(f):
        try:
            print(sp.printing.mathml(sp.acoth(x)))
            print(sp.printing.mathml(sp.acsc(x)))
            print(sp.printing.mathml(sp.asec(x)))
        except AssertionError as e:
            print_stacktrace(e)
            raise

if __name__ == "__main__":
    x = sp.Symbol('x')
    reproduce_issue()
```

You can run this script by executing `python3 reproducer.py` in the root directory of your project. If the issue is present, it will print a stack trace and raise an `AssertionError`.