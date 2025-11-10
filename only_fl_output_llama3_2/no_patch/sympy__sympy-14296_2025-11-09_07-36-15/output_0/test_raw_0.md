Here is the standalone Python file `reproducer.py` that reproduces the issue:

```python
import sympy as sp
from reproducer import print_stacktrace

def reproduce_issue():
    b = 1 - sp.sqrt(2)
    a = sp.to_number_field(b)
    assert minimal_polynomial(a) == 'x**2 + 2*x - 1', "Issue: Minimal polynomial of algebraic number is incorrect"
    raise AssertionError("Issue reproduced")

try:
    reproduce_issue()
except AssertionError as e:
    print_stacktrace(e)
    exit(0)

def minimal_polynomial(x):
    return sp.poly(x.minpoly).as_expr()

if __name__ == "__main__":
    reproduce_issue()
```

This script will run the `reproduce_issue` function, which creates an algebraic number and then checks if its minimal polynomial is correct. If not, it raises an `AssertionError`, which is caught by the script and printed with a stack trace.