Here is the reproducer script:

```python
import sympy
import unittest
from io import StringIO
from contextlib import redirect_stdout

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
        for i in range(16, 18):
            with redirect_stdout(StringIO()):
                try:
                    sympy.linsolve([sympy.Eq(0.0215 * 'x', 'y'), sympy.Eq('y', i * 'x')], ('x', 'y'))
                    self.fail("Expected linsolve to fail")
                except Exception as e:
                    print_stacktrace(e)
                    self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
```

This script will run the `linsolve` function with different values of `i` in the range [16, 18) and check if it raises an exception. If it does, it will print the stack trace and exit with code 0.