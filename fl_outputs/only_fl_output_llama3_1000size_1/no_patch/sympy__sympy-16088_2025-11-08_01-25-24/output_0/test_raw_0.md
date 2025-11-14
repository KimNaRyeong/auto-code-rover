Here is the reproducer script:

```python
import sympy as sp
from assertpy import assert_that

def reproduce_issue():
    x = sp.symbols('x')
    y = sp.symbols('y')
    n = sp.symbols('n')

    integral = sp.Integral(x*y, (x, 1, n)).simplify()
    assert_that(integral).is_not_equal_to(sp.Integral(y*x, (x, 1, n)))

if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        exit(0)
```

This script creates a symbolic integral with `x*y` and simplifies it. If the issue is present, it should raise an `AssertionError`. The script then prints the stack trace using the provided function and exits with code 1. If the issue is fixed, it simply exits with code 0.