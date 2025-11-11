Here is the reproducer script:

```python
import sympy as sp
from sympy.integrals import Integral

def reproduce_issue():
    x = sp.symbols('x')
    y = sp.symbols('y', cls=sp.Function)
    n = sp.symbols('n')

    integral = Integral(x*y, (x, 1, n))
    try:
        simplified_integral = integral.simplify()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")

    if str(simplified_integral) != "n      \n⌠\n y⋅⎮ x dx\n⌡     \n  1":
        raise AssertionError("Issue not fixed")

if __name__ == "__main__":
    reproduce_issue()
```

This script defines the `reproduce_issue` function, which creates a symbolic integral using Sympy. It then attempts to simplify the integral and checks if the result matches the expected output. If the issue is present (i.e., the simplification does not pull out the constant term), it prints the stack trace and raises an `AssertionError`.