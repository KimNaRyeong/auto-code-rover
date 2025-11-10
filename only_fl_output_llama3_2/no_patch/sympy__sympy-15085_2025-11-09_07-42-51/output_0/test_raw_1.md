Here is the reproducer script:

```python
import sympy
from sympy import Matrix, symbols

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

try:
    x = symbols("x")
    expr = Matrix([[2], [1], [0]]) * x
    f = sympy.lambdify(x, expr)
    X = [[1]]
    val = f(X)
    assert "NameError: name 'Matrix' is not defined" in str(type(Exception())), "Expected NameError: name 'Matrix' is not defined"

except Exception as e:
    print_stacktrace(e)
    exit(0)

print("Issue reproduced successfully.")
```

This script will reproduce the issue by attempting to create a lambda function from a sympy expression that involves a dot product with a `sympy.Matrix`. If the issue is present, it will print the stack trace and exit with code 0.