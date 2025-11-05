Here is the reproducer script:

```python
import sys
from pylint.lint import Run
from pylint.config.exceptions import _UnrecognizedOptionError
from io import StringIO
import unittest

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