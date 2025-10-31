Here is the reproducer script:

```python
import sympy as sp
from assertpy import assert_that

def main():
    try:
        result = sp.degree((sp.Symbol('x') - 2) / ((sp.Symbol('x'))**2 + 1), sp.Symbol('x'))
        assert_that(result).is_equal_to(1)
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
```

This script will attempt to compute the degree of a rational function using SymPy, and if it fails, it will print the stack trace and raise an `AssertionError`.