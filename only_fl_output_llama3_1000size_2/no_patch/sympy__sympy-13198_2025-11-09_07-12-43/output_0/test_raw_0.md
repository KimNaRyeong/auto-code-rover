Here is the reproducer script:

```python
import sympy as sp
from sympy.abc import x, y, z
import unittest

def test_issue():
    w = 0.0001 * (x * (x + (4.0 * y))) + 0.0001 * (y * (x + (4.0 * y)))
    v = sp.factor(w)
    assert str(sp.expand(v)) == "1e-8*x**2 + 5e-8*x*y + 4e-8*y**2", f"Expected {str(sp.expand(v))} but got {v}"
    print_stacktrace(AssertionError)

class TestIssue(unittest.TestCase):
    def test_issue(self):
        test_issue()

if __name__ == "__main__":
    test_issue()
```

This script will raise an `AssertionError` if the issue is present, and it will print a stack trace with line numbers.