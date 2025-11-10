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
    sp.init_printing(use_latex=False)
    x = sp.symbols('x')
    y = sp.symbols('y')
    n = sp.symbols('n')

    try:
        result = sp.Sum(x*y, (x, 1, n)).simplify()
        f = StringIO()
        with redirect_stdout(f):
            print(result)
        output = f.getvalue().strip()
        if "⌠" in output and "⎮" not in output:
            raise AssertionError("Expected the constant term to be pulled out")
    except Exception as e:
        print_stacktrace(e)

if __name__ == "__main__":
    reproduce_issue()
```

This script will run the given code, check if the expected behavior is observed (i.e., the constant term is not pulled out), and raise an `AssertionError` with a stack trace if the issue is present.