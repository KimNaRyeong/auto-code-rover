Here is the standalone Python file `reproducer.py` that reproduces the issue:

```python
import sympy
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
        from sympy import Matrix
        x = sympy.Symbol("x")
        expr = Matrix([[2], [1], [0]]) * x
        f = sympy.lambdify(x, expr)
        X = numpy.zeros((17, 3))
        val = f(X)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    reproduce_issue()
```

This script attempts to create a lambda function from a sympy expression that involves a dot product with a `sympy.Matrix`. If the issue is present, it will print the stack trace and raise an `AssertionError`.