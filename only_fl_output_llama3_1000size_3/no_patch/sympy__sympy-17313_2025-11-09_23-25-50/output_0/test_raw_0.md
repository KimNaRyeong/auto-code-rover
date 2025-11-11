Here is the reproducer script:

```python
import math
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

class TestMathFunctions(TestCase):
    def test_ceiling_and_floor(self):
        self.assertGreater(math.ceil(-1), 0)
        self.assertLess(math.floor(-1), 0)
        self.assertGreaterEqual(math.ceil(1), 0)
        self.assertGreaterEqual(math.floor(1), 0)

if __name__ == "__main__":
    try:
        suite = unittest.TestLoader().loadTestsFromTestCase(TestMathFunctions)
        runner = unittest.TextTestRunner()
        result = runner.run(suite)
        if not any((not ok) for ok in result.wasSuccessful()):
            print("Issue reproduced.")
            raise AssertionError
        else:
            print("No issue found.")
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```

This script defines a test case that checks the ceiling and floor functions for negative and positive numbers. If any of these assertions fail, it prints the stack trace and exits with code 1.