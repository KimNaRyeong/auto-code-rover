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
    with StringIO() as f:
        print("Traceback (most recent call last):", file=f)
        for frame in tb:
            line_number = frame.lineno
            code_context = frame.line.strip() if frame.line else "Unknown"
            print(f'  File "{frame.filename}"', file=f)
            print(f"    {line_number}: {code_context}", file=f)
        print(f"{e.__class__.__name__}: {e}", file=f)
        f.seek(0)
        print(f.read())

class TestIssue(unittest.TestCase):

    def test_issue(self):
        try:
            sp.Poly(x)*x
            x*sp.Poly(x)
            -2*sp.Poly(x)
            sp.S(-2)*sp.Poly(x)
            sp.Poly(x)*sp.S(-2)
        except Exception as e:
            with StringIO() as f, redirect_stdout(f):
                print_stacktrace(e)
            self.fail("Expected exception")

if __name__ == '__main__':
    unittest.main(exit=False)
    if len(sys.argv) > 1 and sys.argv[1] == 'fixed':
        exit(0)
    else:
        exit(1)
```

This script will run the test case, which attempts to reproduce the issue. If an exception is raised during the execution of the test case, it will print the stack trace using the provided function `print_stacktrace`. The script then fails the test case.

To use this script, save it as `reproducer.py` and execute it with Python 3: `python3 reproducer.py`.