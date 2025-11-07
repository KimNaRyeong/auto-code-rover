Here is the reproducer script:
```python
import os
import sys
from unittest import main, TestCase
import traceback

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
        try:
            import pylint
            pylint.pyreverse(output='png', project='test_project', files=['file1.py', 'file2.py'])
        except ModuleNotFoundError as e:
            print_stacktrace(e)
            self.fail("Expected error")
        else:
            raise AssertionError("Error not raised")

if __name__ == "__main__":
    main()
```
This script attempts to run `pylint.pyreverse` with the same arguments you provided. If a `ModuleNotFoundError` is raised, it prints the stack trace and fails the test. If no exception is raised, it raises an assertion error.

To reproduce the issue, simply execute this script using Python: `python3 reproducer.py`.