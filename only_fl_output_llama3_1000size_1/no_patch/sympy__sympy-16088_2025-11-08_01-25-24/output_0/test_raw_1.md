Here is the reproducer script:

```python
import sympy as sp

def reproduce_issue():
    x = sp.symbols('x')
    y = sp.symbols('y')
    n = sp.symbols('n')

    integral = sp.Integral(x*y, (x, 1, n)).doit().simplify()
    assert_that(integral).is_not_equal_to(sp.Integral(y*x, (x, 1, n)))

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
    try:
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        exit(0)
```

This script creates a symbolic integral with `x*y` and simplifies it. If the issue is present, it should raise an `AssertionError`. The script then prints the stack trace using the provided function and exits with code 1. If the issue is fixed, it simply exits with code 0.