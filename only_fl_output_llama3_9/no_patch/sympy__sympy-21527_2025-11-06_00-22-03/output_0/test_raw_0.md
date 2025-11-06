Here is the reproducer script:

```python
import sympy
import unittest
from io import StringIO
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class TestLinsolve(unittest.TestCase):

    def test_linsolve(self):
        for i in range(0.0215, 0.0217, 0.0001):
            try:
                x,y = sympy.symbols('x, y')
                result = sympy.linsolve([sympy.Eq(y, x), sympy.Eq(y, i * x)], (x, y))
                if not isinstance(result, sympy.sets.FiniteSet) or len(list(result)) > 1:
                    raise AssertionError("linsolve failed")
            except Exception as e:
                print_stacktrace(e)
                self.fail()

if __name__ == '__main__':
    unittest.main()
```

This script runs a test case where it iterates over the values of `i` from `0.0215` to `0.0217` with increments of `0.0001`. For each value, it tries to solve the system of equations using `sympy.linsolve`. If the result is not a single point (i.e., a finite set containing only one element), or if an exception occurs during the execution of `linsolve`, the script raises an `AssertionError` and prints the stack trace.