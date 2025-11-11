Here is the reproducer script:

```python
import sympy
from sympy import Matrix, Symbol
import numpy

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
        from sympy import lambdify
        x = Symbol("x")
        expr = lambdify(x, x * Matrix([[2], [1], [0]]))
        X = numpy.zeros((17, 3))
        val = expr(X)
    except Exception as e:
        print_stacktrace(e)
        assert False, "Issue reproduced"

if __name__ == "__main__":
    reproduce_issue()
```

This script should raise an `AssertionError` when the issue is present and print a stack trace of the issue.