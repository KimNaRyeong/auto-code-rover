Here is the reproducer script:

```python
import sympy as sp
from sympy.abc import y, x, f

def idiff(expr, var, other):
    try:
        return sp.idiff(expr, var, other)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected the issue to be present")

idiff(Eq(y*sp.exp(y), x*sp.exp(x)), y, x)
idiff(f(x)*sp.exp(f(x)) - x*sp.exp(x), f(x), x)
idiff(y*sp.exp(y) - x*sp.exp(x), y, x)

```

This script will reproduce the issue by calling `idiff` with different inputs and print a stack trace if any of them raise an exception.