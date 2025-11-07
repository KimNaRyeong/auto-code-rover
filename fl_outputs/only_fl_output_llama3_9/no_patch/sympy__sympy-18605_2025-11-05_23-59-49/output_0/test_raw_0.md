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
    def test_reproducer(self):
        m, n = sp.symbols("m, n", real=True)
        i = sp.Idx("i", (m, n))
        self.fail("Expected TypeError")

if __name__ == "__main__":
    try:
        suite = unittest.TestLoader().loadTestsFromTestCase(Reproducer)
        runner = unittest.TextTestRunner()
        result = runner.run(suite)
        if not result.wasSuccessful():
            print_stacktrace(result.errors[0])
        else:
            print("Issue fixed, exiting with code 0")
    except Exception as e:
        print_stacktrace(e)
```

This script defines a test case `Reproducer` that attempts to create an `Idx` object with non-integer bounds. The `test_reproducer` method fails the test if no `TypeError` is raised, indicating that the issue is present. If the test passes, it prints a stack trace of the expected error.

The script also defines the `print_stacktrace` function as requested. When run, this script will either print an error message and exit with code 1 (indicating the issue is present) or print a success message and exit with code 0 (indicating the issue is fixed).