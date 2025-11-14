Here is the reproducer script:

```python
import sympy as sp
from unittest import TestCase

class Reproducer(TestCase):
    def test_quaternion_evalf(self):
        q = sp.Quaternion(1/sp.sqrt(2), 0, 0, 1/sp.sqrt(2))
        try:
            q.evalf()
        except AttributeError as e:
            print_stacktrace(e)
            self.fail("Quaternion class has no overridden evalf method")

if __name__ == "__main__":
    test_result = Reproducer().run()
    if not test_result.wasSuccessful():
        exit(1)
    else:
        exit(0)

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

```

This script will run the test case and if the `evalf` method is not overridden in the `Quaternion` class, it will raise an `AssertionError`, print the stack trace using the provided function, and then exit with code 1. If the issue is fixed, it will exit with code 0.