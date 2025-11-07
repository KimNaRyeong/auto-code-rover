Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
import sympy
from sympy.core.power import isqrt

def main():
    n = 4503599761588224
    s = isqrt(n)
    assert s**2 <= n, "isqrt gives incorrect results"
    if not s**2 <= n:
        raise AssertionError("isqrt gives incorrect results")
        print_stacktrace(AssertionError)

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```

This script will reproduce the issue by calling `isqrt` with the given input and asserting that the result is correct. If the assertion fails, it will raise an `AssertionError`, which will be caught and printed along with a stack trace.