Here is the reproducer script:

```python
import sys
from pylint.lint import Run
from pylint.config.exceptions import _UnrecognizedOptionError
from io import StringIO
import unittest
import traceback
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    try:
        Run(['-Q'])
    except _UnrecognizedOptionError as e:
        print_stacktrace(e)
        raise AssertionError("Issue should not be present")

if __name__ == "__main__":
    main()
```

This script attempts to run Pylint with the `-Q` option, which is an unrecognized option. If an error occurs, it prints the stack trace and raises an `AssertionError`.