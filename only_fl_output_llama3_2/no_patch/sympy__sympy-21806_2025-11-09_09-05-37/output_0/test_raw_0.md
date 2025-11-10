Here is the reproducer script:

```python
import sympy as sp
from unittest import TestCase

class Reproducer(TestCase):
    def test_quaternion_evalf(self):
        try:
            q = sp.Quaternion(1/sp.sqrt(2), 0, 0, 1/sp.sqrt(2))
            q.evalf()
        except AttributeError as e:
            print_stacktrace(e)
            raise AssertionError("Quaternion class has no overridden evalf method")

if __name__ == "__main__":
    suite = unittest.TestSuite([Reproducer()])
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    if not result.wasSuccessful():
        sys.exit(1)

```

This script creates a test case that attempts to call the `evalf` method on a `Quaternion` object. If an `AttributeError` is raised, it prints the stack trace and raises an `AssertionError`.