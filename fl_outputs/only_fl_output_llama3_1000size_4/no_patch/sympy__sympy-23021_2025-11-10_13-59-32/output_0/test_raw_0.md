Here is the reproducer script:

```python
import sympy as sp
from sympy import Min, Poly

def decompogen_test():
    x = sp.symbols('x')
    try:
        result = sp.decompogen(Min(5,x), x)
        print(result)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected decompogen to work with Min/Max")

if __name__ == "__main__":
    decompogen_test()
```

This script will attempt to run the `decompogen` function on the expression `Min(5,x)` and symbol `x`. If an exception is raised, it will print the stack trace using the provided function and then raise an `AssertionError`.