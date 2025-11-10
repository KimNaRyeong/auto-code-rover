Here is the reproducer script:

```python
import sympy as sp
from unittest import TestCase

class Reproducer(TestCase):
    def test_issue(self):
        try:
            with sp.evaluate(False):
                sp.S('Point2D(Integer(1),Integer(2))')
            self.fail("Expected ValueError")
        except Exception as e:
            print_stacktrace(e)
            raise AssertionError("Issue not present")

if __name__ == "__main__":
    Reproducer().test_issue()
```

This script will run the test case and if the issue is present, it will print the stack trace and exit with code 1. If the issue is fixed, it will fail the test case and exit with code 0.