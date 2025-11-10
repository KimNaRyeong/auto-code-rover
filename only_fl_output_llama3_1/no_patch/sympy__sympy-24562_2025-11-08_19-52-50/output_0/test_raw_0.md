Here is the reproducer script:

```python
import sympy
from unittest import TestCase

class Reproducer(TestCase):
    def test_rational_calc_value_error(self):
        try:
            rational = sympy.Rational('0.5', '100')
            self.assertEqual(rational, sympy.Rational(1, 200))
        except Exception as e:
            print_stacktrace(e)
            raise

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(Reproducer('test_rational_calc_value_error'))
    result = unittest.TextTestRunner().run(suite)
    if any(not test.result.wasSuccessful() for test in suite):
        sys.exit(1)
```

This script creates a simple unit test that attempts to create a `Rational` object with the given values. If an exception is raised, it prints the stack trace and raises the same exception again. If no exception is raised, it exits with code 0.

To run this script, save it in a file named `reproducer.py`, then execute it using `python3 reproducer.py`.