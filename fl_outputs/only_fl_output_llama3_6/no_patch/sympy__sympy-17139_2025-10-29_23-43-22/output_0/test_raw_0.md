Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
import sympy as sp
from sympy import *

def main():
    x = Symbol('x')
    try:
        print(simplify(cos(x)**I))
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")

if __name__ == "__main__":
    main()
```

This script will execute the same code that reproduces the issue and then print a stack trace if an exception is raised.