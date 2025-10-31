Here is the reproducer script:

```python
import sympy as sp
from sympy import zoo

def main():
    try:
        sp.frac(zoo)
    except TypeError as e:
        print_stacktrace(e)
        raise AssertionError("Expected TypeError")

if __name__ == "__main__":
    main()
```

You can run this script by executing `python3 reproducer.py`. If the issue is present, it will print a stack trace and then raise an assertion error.