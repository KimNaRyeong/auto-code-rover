Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
import sympy as sp
from reproducer import print_stacktrace

def main():
    b = 1 - sp.sqrt(2)
    a = sp.to_number_field(b)
    if not (a.minpoly == sp.Poly(sp.Pow(a.gen, 2) + 2*sp.Pow(a.gen, 1) - 1)):
        raise AssertionError("Issue present")
    print_stacktrace(AssertionError("Issue fixed"))

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(0)
```

This script will run the same code that reproduces the issue, and if the issue is present (i.e., the minimal polynomial of `a` is not correct), it will raise an `AssertionError`. If the issue is fixed, it will print a message indicating that the issue was fixed.