Here is the reproducer script:

```python
import sympy as sp
from sympy.abc import x, y
import unittest
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

class TestConditionSet(unittest.TestCase):

    def test_condition_set(self):
        try:
            c = sp.ConditionSet(x, x > 5, sp.Interval(1, 7))
            self.assertEqual(c.subs(x, 8), sp.EmptySet())
        except Exception as e:
            print_stacktrace(e)
            raise

if __name__ == '__main__':
    unittest.main()
```

This script will run the test case and if any exception is raised during the execution of the test case, it will print the stack trace.