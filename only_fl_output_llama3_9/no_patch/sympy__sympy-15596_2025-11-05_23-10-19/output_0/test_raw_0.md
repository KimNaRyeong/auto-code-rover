Here is the reproducer script:

```python
import sympy as sp
from unittest import TestCase
import sys

def print_stacktrace(e: Exception):
    import traceback
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
            f = sp.Rational((x-2)/(x**2+1), x)
            degree(f, x)
        except Exception as e:
            print_stacktrace(e)
            raise

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(Reproducer)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    if not result.wasSuccessful():
        sys.exit(1)

```

This script defines a test case that attempts to compute the degree of a rational function using SymPy. If an exception is raised, it prints the stack trace and raises the same exception again.