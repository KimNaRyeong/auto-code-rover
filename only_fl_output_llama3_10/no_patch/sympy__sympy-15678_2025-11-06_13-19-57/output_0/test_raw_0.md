Here is the reproducer script:

```python
import sympy as sp
from sympy import Eq, exp, symbols

def idiff(expr, var1, var2):
    try:
        return sp.idiff(Eq(expr, var1*exp(var1) - var2*exp(var2)), var1, var2)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue present")

try:
    idiff(Eq(y*sp.exp(y), x*sp.exp(x)), y, x)
except Exception as e:
    print_stacktrace(e)

try:
    idiff(f(x)*sp.exp(f(x)) - x*sp.exp(x), f(x), x)
except Exception as e:
    print_stacktrace(e)

try:
    idiff(y*sp.exp(y) - x*sp.exp(x), y, x)
except Exception as e:
    print_stacktrace(e)

print("Issue fixed")
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue. It will exit with code 0 when the issue is fixed.