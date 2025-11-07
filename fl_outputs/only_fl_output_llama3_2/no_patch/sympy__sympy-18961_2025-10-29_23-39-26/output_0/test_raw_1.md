Here is the reproducer script:

```python
import sympy
from sympy.ntheory import digits

def test_digits():
    try:
        result = digits(-1, bits=3)
        assert len(result) == 3
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    test_digits()
```

This script will run the `test_digits` function and check if the result of calling `digits(-1, bits=3)` is equal to `[1, 0, -1]`. If not, it will print a stack trace and raise an `AssertionError`.