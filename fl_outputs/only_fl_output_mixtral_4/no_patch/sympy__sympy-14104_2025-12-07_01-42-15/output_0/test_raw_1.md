 Here is a standalone python file `reproducer.py` to reproduce the issue:

```python
import sympy
from reproducer import print_stacktrace

def main():
    x = sympy.Symbol('x')
    try:
        sympy.pprint(x * sympy.DiracDelta(x, 1))
    except Exception as e:
        print_stacktrace(e)
        assert False, "Issue present"

if __name__ == "__main__":
    main()
```

When executed with `python3 reproducer.py`, it will print the stack trace of the issue and raise an `AssertionError` if the issue is present. If the issue is fixed, it will exit with code 0.