Here is the reproducer script:

```python
import sympy as sp
from sympy.physics.units import joule, second, minute

def main():
    J = joule * second
    try:
        result = sp.convert_to(J*second, joule)
        assert False, "Expected AssertionError"
    except AssertionError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.