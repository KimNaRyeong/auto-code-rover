Here is the reproducer script:

```python
import sympy as sp
from unittest import TestCase

class Reproducer(TestCase):
    def test_degree(self):
        try:
            result = sp.degree((sp.Symbol('x')-2)/(sp.sympify('x**2+1')), sp.Symbol('x'))
            self.fail("Expected AssertionError")
        except AssertionError as e:
            print_stacktrace(e)

if __name__ == "__main__":
    test_case = Reproducer()
    test_case.test_degree()
```

This script defines a `Reproducer` class that inherits from `TestCase`. The `test_degree` method attempts to compute the degree of the rational function `(x-2)/(x**2+1)` with respect to `x`, and if it succeeds, it fails the test. If an `AssertionError` is raised instead, it prints the stack trace using the provided function.

To run this script, save it as `reproducer.py` in the root directory of your project and execute it with `python3 reproducer.py`.