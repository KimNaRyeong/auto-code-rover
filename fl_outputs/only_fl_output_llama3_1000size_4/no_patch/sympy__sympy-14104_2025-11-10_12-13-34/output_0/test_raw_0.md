Here is the reproducer script:

```py
import sympy as sp
from pprint import pprint

def main():
    x = sp.symbols('x')
    try:
        pprint(x*sp.DiracDelta(x, 1))
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    main()
```

This script will reproduce the issue by calling `pprint(x*DiracDelta(x, 1))`. If the issue is present, it will print a stack trace and then raise an `AssertionError` to indicate that the issue was successfully reproduced.