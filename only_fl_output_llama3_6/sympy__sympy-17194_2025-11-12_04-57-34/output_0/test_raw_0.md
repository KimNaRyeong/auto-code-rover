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
            assert sp.printing.mathml(sp.acoth(x)) == '<apply><arccoth/><ci>x</ci></apply>'
            assert sp.printing.mathml(sp.acsc(x)) == '<apply><arccsc/><ci>x</ci></apply>'
            assert sp.printing.mathml(sp.asec(x)) == '<apply><arcsec/><ci>x</ci></apply>'
        except AssertionError as e:
            print_stacktrace(e)
            exit(1)

if __name__ == "__main__":
    x = sp.Symbol('x')
    reproduce_issue()
```

This script defines a function `reproduce_issue` that attempts to reproduce the issue by calling the `mathml` function with the given expressions. If any of the assertions fail, it prints the stack trace and exits with code 1.