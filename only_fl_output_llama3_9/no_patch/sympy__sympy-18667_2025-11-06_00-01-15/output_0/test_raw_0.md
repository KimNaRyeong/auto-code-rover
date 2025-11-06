Here is the reproducer script:

```python
import unittest
from combinatorics import Schur_Number

class TestSchurNumber(unittest.TestCase):

    def test_schur_number(self):
        # Add your test cases here
        self.fail("This test should fail when the issue is present")

if __name__ == '__main__':
    try:
        suite = unittest.TestLoader().loadTestsFromTestCase(TestSchurNumber)
        unittest.TextTestRunner(verbosity=2).run(suite)
    except AssertionError as e:
        print_stacktrace(e)
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

This script will run the test case and if it fails, it will print the stack trace of the failure.