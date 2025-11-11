Here is the reproducer script:

```python
import sympy as sp
from sympy.abc import x
import unittest
from io import StringIO
from contextlib import redirect_stdout

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    with open('stacktrace.txt', 'w') as f:
        print("Traceback (most recent call last):", file=f)
        for frame in tb:
            line_number = frame.lineno
            code_context = frame.line.strip() if frame.line else "Unknown"
            print(f'  File "{frame.filename}"', file=f)
            print(f"    {line_number}: {code_context}", file=f)
        print(f"{e.__class__.__name__}: {e}", file=f)

class TestPolyMultiplication(unittest.TestCase):

    def test_poly_multiplication(self):
        try:
            sp.Poly(x)*x
            x*sp.Poly(x)
            -2*sp.Poly(x)
            sp.S(-2)*sp.Poly(x)
            sp.Poly(x)*sp.S(-2)
        except Exception as e:
            f = StringIO()
            with redirect_stdout(f):
                print_stacktrace(e)
            self.fail("Expected no exception, but got: \n" + f.getvalue())

if __name__ == '__main__':
    unittest.main()
```

This script will run the given expressions and catch any exceptions that are raised. If an exception is caught, it will print the stack trace to a file named `stacktrace.txt`.