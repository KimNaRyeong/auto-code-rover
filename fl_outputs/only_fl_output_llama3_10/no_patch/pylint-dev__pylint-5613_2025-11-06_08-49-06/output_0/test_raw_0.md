Here is the reproducer script:
```python
import pylint
from unittest import main, TestCase
import sys
import os
import traceback
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

class Reproducer(TestCase):
    def test_reproducer(self):
        name = "test_project"
        files = ["file1.py", "file2.py"]
        try:
            pylint.run_pyreverse()
        except SystemExit as e:
            print_stacktrace(e)
            self.fail("Expected error")
        else:
            raise AssertionError("Error not raised")

if __name__ == "__main__":
    main()
```
This script defines a test case that attempts to run `pylint.pyreverse` with the same arguments you provided. If an exception is raised, it prints the stack trace and fails the test. If no exception is raised, it raises an assertion error.

To reproduce the issue, simply execute this script using Python: `python3 reproducer.py`.