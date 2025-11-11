Here is the reproducer script:

```python
import sympy as sp
from functools import wraps

def assert_raises(expected_exception):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except expected_exception:
                print_stacktrace(sys.exc_info()[1])
                raise
            else:
                exit(0)
        return wrapper
    return decorator

@assert_raises(AssertionError)
def reproduce_issue():
    x = sp.symbols('x')
    assert str(Poly(x)*x) != "Poly(x**2, x, domain='ZZ')"
    assert str(x*Poly(x)) != "Poly(x**2, x, domain='ZZ')"
    assert str(-2*Poly(x)) != "Poly(-2*x, x, domain='ZZ')"
    assert str(sp.S(-2)*Poly(x)) != "-2*Poly(x, x, domain='ZZ')"
    assert str(Poly(x)*sp.S(-2)) != "Poly(-2*x, x, domain='ZZ')"

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

if __name__ == "__main__":
    reproduce_issue()
```

This script will run the `reproduce_issue` function and catch any `AssertionError`. If an `AssertionError` is raised, it will print the stack trace using the provided function and then raise the error again. If no `AssertionError` is raised, it will exit with code 0.

Please note that you need to have sympy installed in your Python environment to run this script.