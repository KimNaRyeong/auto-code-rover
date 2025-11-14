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

You can run this script by executing `python3 reproducer.py`. If the issue is present, it will print a stack trace and exit with code 1.