Here is the reproducer script:

```python
import QQ.frac_field as FF
from unittest import TestCase

class Reproducer(TestCase):
    def test_issue(self):
        x = 1.0 / 2.0
        self.assertRaises(AssertionError, lambda: not in FF.QQ.frac_field(x))

if __name__ == "__main__":
    try:
        Reproducer().test_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Issue fixed")
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

This script will run the test case, and if an `AssertionError` is raised, it will print the stack trace using the provided function. If no error is raised, it will print a success message and exit with code 0.