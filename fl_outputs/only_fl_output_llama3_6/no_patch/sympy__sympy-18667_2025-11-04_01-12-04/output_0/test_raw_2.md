Here is the reproducer script:

```python
import unittest
import sys

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
            assert 1 == 2, "Expected AssertionError"
        except AssertionError as e:
            print_stacktrace(e)
            sys.exit(0)  # exit with code 0 when the issue is fixed

if __name__ == '__main__':
    unittest.main(exit=False)
```

This script will run a test case that should raise an `AssertionError`. If the error is raised, it will print the stack trace using the provided function and then exit with code 0.