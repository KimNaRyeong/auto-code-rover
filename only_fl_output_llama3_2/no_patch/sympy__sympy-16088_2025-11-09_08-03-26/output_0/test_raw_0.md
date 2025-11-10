Here is the reproducer script:

```python
import sympy as sp
from sympy.integrals import Integral

def reproduce_issue():
    x = sp.symbols('x')
    y = sp.Function('y')
    n = sp.Symbol('n')

    integral = Integral(x*y, (x, 1, n))
    try:
        simplified_integral = integral.simplify()
        assert False, "Expected an assertion error"
    except AssertionError:
        pass
    finally:
        print_stacktrace(sys.exc_info()[0])

if __name__ == "__main__":
    reproduce_issue()
```

This script creates a symbolic expression for the integral and attempts to simplify it. If the issue is present, it should raise an `AssertionError` which will be caught by the script and printed with a stack trace.