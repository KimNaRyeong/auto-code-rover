Here is the reproducer script:

```python
import sympy as sp
from sympy.abc import z, pi

def reproduce_issue():
    try:
        result = sp.polylog(2, sp.Rational(1, 2)).expand(func=True).evalf()
        expected_result = -sp.log(2)**2/2 + pi**2/12
        if not sp.simplify(result - expected_result) == 0:
            raise AssertionError("Issue present")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script will attempt to reproduce the issue by expanding and evaluating `polylog(2, Rational(1/2))`. If the result is not equal to the expected value `-log(2)**2/2 + pi**2/12` after simplification, it will raise an `AssertionError`, print a stack trace using the provided function, and exit with code 1.