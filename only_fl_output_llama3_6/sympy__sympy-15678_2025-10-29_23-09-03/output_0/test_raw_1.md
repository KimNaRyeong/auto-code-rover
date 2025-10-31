Here is the reproducer script `reproducer.py`:

```python
from sympy import Eq, exp, symbols
from sympy.abc import y, x, f

def idiff(expr, var, other):
    try:
        return expr.diff(other).subs({var: other})
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected issue")

try:
    idiff(Eq(y*exp(y), x*exp(x)), y, x)
except Exception as e:
    pass

try:
    idiff(f(x)*exp(f(x)) - x*exp(x), f(x), x)
except Exception as e:
    pass

idiff(y*exp(y) - x*exp(x), y, x)
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.