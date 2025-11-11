Here is the reproducer script:

```python
import sympy as sp
from sympy import MatrixSymbol, pprint, latex
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
        A = sp.MatrixSymbol('A', 2, 2)
        B = sp.MatrixSymbol('B', 2, 2)
        f = StringIO()
        with redirect_stdout(f):
            print(A - A*B - B)
            pprint(A - A*B - B)
            latex(A - A*B - B)
        output = f.getvalue().strip()
        if "(-1)*" in output:
            raise AssertionError("Issue present")
    except Exception as e:
        print_stacktrace(e)
        exit(0)

if __name__ == "__main__":
    reproduce_issue()
```

This script will execute the given code and check if the issue is present. If the issue is present, it will print a stack trace of the issue and exit with code 0.