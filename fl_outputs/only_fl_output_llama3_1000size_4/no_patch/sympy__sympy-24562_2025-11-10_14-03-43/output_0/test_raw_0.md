Here is the reproducer script:

```python
import sympy
from unittest import TestCase

class Reproducer(TestCase):
    def test_rational_calc_value_error(self):
        try:
            sympy.Rational('0.5', '100')
            self.fail("Expected RationalCalcValueError")
        except Exception as e:
            print_stacktrace(e)
            raise AssertionError("Rational calc value error not reproduced")

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(Reproducer)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    if result.wasSuccessful():
        sys.exit(0)
```

This script creates a test case that attempts to create a `Rational` object with the arguments `'0.5'` and `'100'`. If this operation succeeds, it fails the test. If an exception is raised (which should be the `RationalCalcValueError`), it prints the stack trace using the provided function and raises an `AssertionError`.

You can run this script by executing `python3 reproducer.py` in your terminal.