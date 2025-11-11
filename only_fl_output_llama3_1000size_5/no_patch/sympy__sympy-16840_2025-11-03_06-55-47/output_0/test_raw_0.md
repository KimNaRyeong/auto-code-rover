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

class Reproducer(TestCase):
    def test_issue(self):
        try:
            math.ceil(2/.5)
        except ZeroDivisionError as e:
            raise AssertionError("Expected 4, got ZeroDivisionError") from e
        else:
            print_stacktrace(AssertionError("Issue not present"))

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(Reproducer('test_issue'))
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    if result.wasSuccessful():
        sys.exit(0)
    else:
        print_stacktrace(result.failures[0])
```

You can run this script using `python3 reproducer.py` and it will either exit with code 0 (if the issue is fixed) or raise an AssertionError and print a stack trace of the issue.