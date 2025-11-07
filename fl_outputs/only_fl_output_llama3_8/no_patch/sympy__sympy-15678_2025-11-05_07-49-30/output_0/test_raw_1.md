Here is the reproducer script:

```python
import sympy as sp
from sympy import Eq, exp, symbols

def idiff(func, var, x):
    try:
        return sp.idiff(Eq(func.subs(var, 'x'), x*exp(x)), var, x)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected issue")

if __name__ == "__main__":
    y = symbols('y')
    f = symbols('f', cls=sp.Function)
    x = symbols('x')

    # Test 1: Eq
    idiff(Eq(y*exp(y), x*exp(x)), y, x)

    # Test 2: f(x) instead of y
    idiff(f(x)*exp(f(x)) - x*exp(x), f(x), x)
```

This script defines a function `idiff` that attempts to reproduce the issue. It then calls this function with different inputs and checks if an exception is raised. If an exception is raised, it prints the stack trace using the provided function and raises an `AssertionError`.