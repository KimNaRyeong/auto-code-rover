Here is the `reproducer.py` script that reproduces the issue:

```python
import unittest
from combinatorics import Schur_Number  # Replace 'combinatorics' with the actual module name

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
        try:
            Schur_Number(1)  # Add your expected result here
        except Exception as e:
            print_stacktrace(e)
            raise

if __name__ == '__main__':
    unittest.main()
```

This script will run the `test_schur_number` test case and if any exception occurs during this test, it will catch that exception, print the stack trace using the provided function, and then re-raise the exception.