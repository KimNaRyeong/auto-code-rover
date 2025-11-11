Here is the reproducer script:

```python
import sympy as sp

def test_reproducer():
    try:
        case = "x**2"
        transformations = [sp.sympify('x')]
        parse_expr(case, transformations=transformations)
        raise AssertionError("Expected TypeError")
    except TypeError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    test_reproducer()
```

This script attempts to call `parse_expr` with a string and an empty list of transformations. The expected behavior is that the script should raise a TypeError when trying to create the `factorial` function with no arguments.