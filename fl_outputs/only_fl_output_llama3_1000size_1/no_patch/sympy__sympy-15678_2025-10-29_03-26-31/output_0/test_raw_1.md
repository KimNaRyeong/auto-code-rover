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

try:
    idiff(Eq(y*sp.exp(y), x*sp.exp(x)), y, x)
except Exception as e:
    print_stacktrace(e)
    assert False, "idiff doesn't support Eq"

try:
    idiff(f(x)*sp.exp(f(x)) - x*sp.exp(x), f(x), x)
except Exception as e:
    print_stacktrace(e)
    assert False, "idiff doesn't support f(x) instead of y"

try:
    result = idiff(y*sp.exp(y) - x*sp.exp(x), y, x)
    assert isinstance(result, sp.Expr), "Expected the result to be an expression"
except Exception as e:
    print_stacktrace(e)
    assert False, "idiff doesn't work correctly for some inputs"

print("All tests passed")
```

This script will reproduce the issue by calling `idiff` with different inputs and check if it raises an exception. If any of them raise an exception, it prints a stack trace and asserts that the expected issue is present.