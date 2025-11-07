Here is the reproducer script `reproducer.py`:
```python
import sympy
from unittest import TestCase

class Reproducer(TestCase):
    def test_ceiling_simplify_inconsistent(self):
        try:
            sympy.sympify('4*ceiling(x/4 - 3/4)', evaluate=False).simplify()
            self.fail("Expected inconsistent behavior")
        except AssertionError as e:
            print_stacktrace(e)
            raise

if __name__ == '__main__':
    Reproducer().run()
```
This script defines a test case `test_ceiling_simplify_inconsistent` that attempts to reproduce the issue. If the issue is present, it raises an `AssertionError` and prints the stack trace using the provided function.

To run the reproducer, simply execute the script: `python3 reproducer.py`. If the issue is present, you should see the stack trace printed to the console.