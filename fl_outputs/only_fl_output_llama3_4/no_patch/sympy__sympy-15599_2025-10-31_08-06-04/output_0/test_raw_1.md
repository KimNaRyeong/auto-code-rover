Here is the reproducer script:

```python
import sympy as sp
from sympy import Mod, Symbol

def reproduce_issue():
    i = Symbol('i', integer=True)

    try:
        assert Mod(3*i, 2) == Mod(i, 2)
    except AssertionError:
        print_stacktrace(sys.exc_info()[1])
        exit(0)
    else:
        raise Exception("Issue not found")
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script will run the assertion `assert Mod(3*i, 2) == Mod(i, 2)` and if it fails (i.e., the issue is present), it will print a stack trace and exit with code 0. If the assertion passes (i.e., the issue is fixed), it will raise an exception and exit with code 1.