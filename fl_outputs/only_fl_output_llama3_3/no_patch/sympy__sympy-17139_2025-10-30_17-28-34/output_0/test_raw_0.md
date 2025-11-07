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
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    main()
```

You can run this script by executing `python3 reproducer.py`. If the issue is present, it will print a stack trace and raise an `AssertionError`.