Here is the reproducer script `reproducer.py`:

```python
import sympy as sp
from sympy import Rational, Mul

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

def reproduce_issue():
    x = sp.symbols('x')
    y = sp.symbols('y')

    try:
        result1 = str(Mul(Rational(1, 2), x + y, evaluate=False))
        result2 = str(Mul(x + y, Rational(1, 2), evaluate=False))

        if result1 != "x + y\n─────\n  2" or not result2.startswith("x + y⋅"):
            raise AssertionError("Issue reproduced")
    except Exception as e:
        print_stacktrace(e)

if __name__ == "__main__":
    reproduce_issue()
```

This script uses the `sympy` library to create symbolic variables `x` and `y`. It then attempts to reproduce the issue by creating two instances of the `Mul` class with different orderings. If the expected output is not produced, an `AssertionError` is raised, which is caught and printed using the provided `print_stacktrace` function.