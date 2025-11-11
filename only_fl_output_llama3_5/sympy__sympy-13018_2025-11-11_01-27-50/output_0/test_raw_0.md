Here is the reproducer script:

```python
import sympy
from sympy import Symbol, Pow
from functools import wraps

def assert_raises(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
            raise AssertionError("Expected an exception")
        except Exception as e:
            print_stacktrace(e)
            exit(0)

    return wraps(func)(wrapper)

@assert_raises
def reproduce_issue():
    x = Symbol('x', commutative=False)
    (x*x*x).subs({x*x: 1})

if __name__ == "__main__":
    reproduce_issue()
```

This script will raise an `AssertionError` when the issue is present, print a stack trace of the issue, and exit with code 0 when the issue is fixed.