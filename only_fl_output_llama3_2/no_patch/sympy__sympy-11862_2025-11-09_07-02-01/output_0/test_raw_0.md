Here is the reproducer script:

```python
import sympy as sp
from sympy.abc import x
import mpmath as mp
import numpy as np
import unittest
from io import StringIO
import sys

class TestIssue(unittest.TestCase):

    def test_issue(self):
        g = sp.sqrt(2) - x
        h = g.evalf(64)
        
        f1 = sp.lambdify(x, g, modules='mpmath')
        f2 = sp.lambdify(x, h, modules='mpmath')

        result1 = f1(np.float64(mp.mpfr(sqrt(2), 64)))
        result2 = f2(np.float64(mp.mpfr(sqrt(2), 64)))

        self.assertAlmostEqual(result1, 0.41421356237309505)
        self.assertAlmostEqual(result2, 0.00000000000000009667293313452913037187168859825586442682332026201917202971226475)

    def test_issue_with_assertion(self):
        g = sp.sqrt(2) - x
        h = g.evalf(64)
        
        f1 = sp.lambdify(x, g, modules='mpmath')
        f2 = sp.lambdify(x, h, modules='mpmath')

        result1 = f1(np.float64(mp.mpfr(sqrt(2), 64)))
        result2 = f2(np.float64(mp.mpfr(sqrt(2), 64)))

        if not (result1 == 0.41421356237309505 and result2 == 0.00000000000000009667293313452913037187168859825586442682332026201917202971226475):
            raise AssertionError("Issue present")
        else:
            print("Issue fixed")

    def test_issue_with_stacktrace(self):
        g = sp.sqrt(2) - x
        h = g.evalf(64)
        
        f1 = sp.lambdify(x, g, modules='mpmath')
        f2 = sp.lambdify(x, h, modules='mpmath')

        try:
            result1 = f1(np.float64(mp.mpfr(sqrt(2), 64)))
            result2 = f2(np.float64(mp.mpfr(sqrt(2), 64)))
        except AssertionError as e:
            print_stacktrace(e)
            raise

if __name__ == "__main__":
    test_issue_with_stacktrace()
```

This script will run the tests and if the issue is present, it will print a stack trace.