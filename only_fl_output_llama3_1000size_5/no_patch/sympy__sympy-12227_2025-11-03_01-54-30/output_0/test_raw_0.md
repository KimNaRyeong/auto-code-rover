Here is the reproducer script:

```python
import sympy as sp
from unittest import TestCase

class FloatReproducer(TestCase):
    def test_float_constructor(self):
        try:
            float_val = sp.Float(1.0, 15)
            self.fail("Expected AssertionError")
        except AssertionError:
            print_stacktrace(sys.exc_info()[1])

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(FloatReproducer)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    if not result.wasSuccessful():
        sys.exit(1)

```

This script creates a test case that attempts to create a `Float` object with the given arguments. If an `AssertionError` is raised, it prints the stack trace and exits with code 0 when the issue is fixed.