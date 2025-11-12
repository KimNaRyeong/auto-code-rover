Here is the reproducer script:

```python
import sympy as sp
import mpmath as mp
from sympy.utilities.lambdify import lambdify
import unittest
import sys

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

class TestIssue(unittest.TestCase):

    def test_issue(self):
        x = sp.symbols('x')
        g = sp.sqrt(2) - x
        h = g.evalf(64)
        
        f1 = lambdify(x, g, modules='mpmath')
        f2 = lambdify(x, h, modules='mpmath')

        result1 = f1(mp.mpf('1.414213562373095048801688724209698078569671875376948073176679738'))
        result2 = f2(mp.mpf('1.414213562373095048801688724209698078569671875376948073176679738'))

        self.assertAlmostEqual(result1, -mp.mpf('0.5857864376269042341255954932839416341441395832123456783499455'))
        self.assertAlmostEqual(result2, mp.mpf('-0.414213562373095048801688724209698078569671875376948073176679738'))

    def test_issue_again(self):
        x = sp.symbols('x')
        g = sp.sqrt(2) - x
        h = g.evalf(64)
        
        f1 = lambdify(x, g, modules='mpmath')
        f2 = lambdify(x, h, modules='mpmath')

        try:
            f1(N(sqrt(2), 64))
        except Exception as e:
            print_stacktrace(e)

    if __name__ == '__main__':
        unittest.main()
```

This script will run two tests. The first test checks the results of `f1` and `f2`. If these results are not equal to the expected values, it means that there is an issue with the precision loss when lambdifying high-precision floats.

The second test tries to reproduce the issue by calling `f1(N(sqrt(2), 64))`. If this call raises an exception, it prints the stack trace of the exception.