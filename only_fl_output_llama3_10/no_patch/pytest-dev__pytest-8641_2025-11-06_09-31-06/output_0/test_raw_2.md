Here is the reproducer script:

```python
import logging
from logging import ColoredLevelFormatter
import pytest
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

def main():
    formatter = ColoredLevelFormatter('%(asctime)s %(funcName)-40.40s L%(lineno)-.4d %(levelname)-5.5s| %(message)s')
    logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%dT%H:%M:%S', format=formatter._format)
    logging.getLogger().setLevel(logging.INFO)

    try:
        pytest.main(['-v', '-s'])
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    except SystemExit as e:
        if e.code != 0:
            print_stacktrace(e)
            sys.exit(1)

if __name__ == "__main__":
    main()
```

This script sets up a basic configuration for the Python logger with the specified format string, then runs pytest with some options. If any exception occurs during this process and its exit code is not 0, it prints the stack trace and exits with code 1.