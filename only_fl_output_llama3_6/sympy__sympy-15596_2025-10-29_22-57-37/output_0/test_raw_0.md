Here is the reproducer script:

```python
import sympy as sp
from unittest import TestCase

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class Reproducer(TestCase):
    def test_degree(self):
        try:
            f = sp.sympify("(x-2)/(x**2+1)")
            degree = sp.degree(f, "x")
            self.assertEqual(degree, 1)
        except Exception as e:
            print_stacktrace(e)
            raise

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(Reproducer("test_degree"))
    result = unittest.TextTestRunner().run(suite)
    if not result.wasSuccessful():
        sys.exit(1)
```

This script will run the test and print a stack trace if an exception is raised.