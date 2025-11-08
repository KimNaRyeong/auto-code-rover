Here is the reproducer script:

```python
import sympy as sp
from unittest import TestCase

class Reproducer(TestCase):
    def test_issue(self):
        b = 1 - sp.sqrt(2)
        a = sp.to_number_field(b)
        self.assertEqual(str(a), '-1 + sqrt(2)')  # positive generator created
        self.assertEqual(str(sp.minimal_polynomial(b)), '_x**2 - 2*_x - 1')
        self.assertNotEqual(str(a.minpoly), str(sp.minimal_polynomial(b)))
        self.assertEqual(str(sp.minimal_polynomial(-1 + sp.sqrt(2))), '_x**2 + 2*_x - 1')

    def run_test(self):
        try:
            self.test_issue()
        except AssertionError as e:
            print_stacktrace(e)
            raise

    def main(self):
        self.run_test()

if __name__ == '__main__':
    Reproducer().main()
```

This script creates the algebraic number `b` and then calls `to_number_field` to create an `AlgebraicNumber` generating the extension field. It then checks if the sign of the generated number is positive, and if the minimal polynomial of `a` is correct. If not, it prints the stack trace of the issue and raises an `AssertionError`.