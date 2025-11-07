Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
import sympy
from sympy.core.power import isqrt

def main():
    n = 4503599761588224
    s = isqrt(n)
    assert s**2 <= n, "isqrt gives incorrect results"
    print_stacktrace(AssertionError("isqrt gives incorrect results"))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        exit(1)

```

This script will raise an `AssertionError` when the issue is present, and it will print a stack trace of the issue.