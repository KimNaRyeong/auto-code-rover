Here is the reproducer script in Python:

```python
import sympy as sp
from functools import wraps

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def reproducer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AssertionError as e:
            print_stacktrace(e)
            raise
    return wrapper

@reproducer
def test_issue():
    x = sp.symbols('x')
    y = sp.symbols('y')
    n = sp.symbols('n', integer=True)

    result1 = sp.Sum(x*y, (x, 1, n)).simplify()
    result2 = sp.Integral(x*y, (x, 1, n)).simplify()

    assert isinstance(result1, sp.Sum) and isinstance(result2, sp.Integral), "Issue present"

if __name__ == "__main__":
    test_issue()
```

This script defines a decorator `reproducer` that catches any `AssertionError` exceptions raised by the decorated function. If an exception is caught, it prints the stack trace using the `print_stacktrace` function and then re-raises the exception.

The `test_issue` function tests whether the issue is present or not. It creates some symbolic variables, defines two expressions (one for sum and one for integral), and checks if they are of the expected types. If they are not, it means the issue is present, and an `AssertionError` is raised.

When you run this script with Python 3, it should print a stack trace if the issue is present or exit successfully if the issue is fixed.