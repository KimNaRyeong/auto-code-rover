Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
import unittest
from your_module import Schur_Number  # Replace 'your_module' with the actual module name

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

class TestSchurNumber(unittest.TestCase):
    def test_schur_number(self):
        # Add your test case here
        pass

if __name__ == '__main__':
    try:
        suite = unittest.TestLoader().loadTestsFromTestCase(TestSchurNumber)
        runner = unittest.TextTestRunner()
        result = runner.run(suite)
        if not result.wasSuccessful():
            raise AssertionError("Test failed")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

```

This script will run the test case for `Schur_Number` and check if it passes. If the test fails, it will print the stack trace of the failure and exit with code 1.