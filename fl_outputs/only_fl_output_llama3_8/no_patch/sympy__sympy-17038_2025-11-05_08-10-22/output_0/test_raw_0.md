Here is the reproducer script:

```python
import sympy
from sympy.core.power import isqrt

def main():
    n = 4503599761588224
    s = isqrt(n)
    assert s**2 <= n, "isqrt gives incorrect results"
    print_stacktrace(AssertionError())

n = 9999999999999999
s = isqrt(n)
assert s**2 <= n, "isqrt gives incorrect results"
print_stacktrace(AssertionError())

if __name__ == "__main__":
    main()
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.