Here is the reproducer script:

```python
import sympy
from unittest import TestCase

class Reproducer(TestCase):
    def test_rational_calc_error(self):
        try:
            rational = sympy.Rational('0.5', '100')
            self.assertEqual(rational, sympy.Rational(1, 200))
        except Exception as e:
            print_stacktrace(e)
            raise
        else:
            exit(0)

if __name__ == "__main__":
    Reproducer().run()
```

This script creates a test case that attempts to create a `Rational` object with the arguments `'0.5'` and `'100'`. If an exception is raised, it prints the stack trace using the provided function and then re-raises the exception. If no exception is raised, it exits with code 0.

To run this script, save it to a file named `reproducer.py`, install the required packages (`sympy`), and then execute it with Python: `python3 reproducer.py`.