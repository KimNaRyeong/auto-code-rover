Here is the reproducer script:

```python
import sympy as sp
from sympy import Symbol, Mod

def reproduce_issue():
    i = Symbol('i', integer=True)
    assert Mod(3*i, 2) != Mod(i, 2)

try:
    reproduce_issue()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
else:
    print("Issue not present")
    exit(0)
```

This script imports the necessary modules from Sympy and defines a function `reproduce_issue` that attempts to reproduce the issue. The function creates a symbolic variable `i`, then asserts that `Mod(3*i, 2)` is not equal to `Mod(i, 2)`. If this assertion fails (i.e., the issue is present), it prints the stack trace and exits with code 1. Otherwise, it prints a message indicating that the issue is not present and exits with code 0.