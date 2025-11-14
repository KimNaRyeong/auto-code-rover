Here is the reproducer script:

```python
import sympy as sp
from unittest import TestCase

class Reproducer(TestCase):
    def test_quaternion_evalf(self):
        q = sp.Quaternion(1/sp.sqrt(2), 0, 0, 1/sp.sqrt(2))
        try:
            q.evalf()
        except AttributeError as e:
            print_stacktrace(e)
            self.fail("Quaternion class has no overridden evalf method")

if __name__ == "__main__":
    suite = unittest.TestSuite([Reproducer()])
    runner = unittest.TextTestRunner(failfast=True)
    result = runner.run(suite)
    if not result.wasSuccessful():
        sys.exit(1)
```

This script defines a test case that attempts to call the `evalf` method on a `Quaternion` object. If the method is not overridden, an `AttributeError` will be raised, which we catch and print using the provided function. The script then fails the test if the issue is present.

To run this script, save it as `reproducer.py` in the root directory of your project and execute it with `python3 reproducer.py`.