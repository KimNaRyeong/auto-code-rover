Here is the reproducer script:

```python
import sympy as sp
from sympy.abc import x, y, f

def idiff(expr, var, other):
    try:
        return sp.idiff(expr, var, other)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected issue")

idiff(Eq(y*sp.exp(y), x*sp.exp(x)), y, x)
idiff(f(x)*sp.exp(f(x)) - x*sp.exp(x), f(x), x)
idiff(y*sp.exp(y) - x*sp.exp(x), y, x)

```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.