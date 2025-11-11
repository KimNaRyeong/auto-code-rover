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
    def test_issue(self):
        x = sp.symbols('x')
        try:
            result1 = Poly(x)*x
            result2 = x*Poly(x)
            result3 = -2*Poly(x)
            result4 = S(-2)*Poly(x)
            result5 = Poly(x)*S(-2)
            self.assertEqual(result1, sp.Poly(x**2, x, domain='ZZ'))
            self.assertEqual(result2, x*sp.Poly(x, x, domain='ZZ'))
            self.assertEqual(result3, sp.Poly(-2*x, x, domain='ZZ'))
            self.assertEqual(result4, -2*sp.Poly(x, x, domain='ZZ'))
            self.assertEqual(result5, sp.Poly(-2*x, x, domain='ZZ'))
        except AssertionError as e:
            print_stacktrace(e)
            raise

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(Reproducer)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    if not result.wasSuccessful():
        sys.exit(1)
```

This script uses the `unittest` module to create a test case that attempts to reproduce the issue. The test case checks that the results of various multiplications involving `Poly` and `S` objects are as expected. If any of these assertions fail, it prints the stack trace using the provided function and then raises an `AssertionError`.