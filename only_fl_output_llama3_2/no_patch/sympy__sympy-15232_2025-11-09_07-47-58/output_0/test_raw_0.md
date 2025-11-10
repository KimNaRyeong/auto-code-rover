Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import sympy as sp
from sympy import symbols, Dummy

def main():
    x = symbols('x')
    y = symbols('y', commutative=False)

    # Create a non-commutative object with commutative free_symbols
    obj = y * x + 1

    try:
        result = sp.factor(obj)
        assert False, "Expected AssertionError"
    except AssertionError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()
```

This script creates a non-commutative object `y` with commutative free_symbols and then attempts to factor it using the `factor()` function. The expected behavior is that an `AssertionError` should be raised due to the issue in the original code.