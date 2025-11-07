Here is the reproducer script:

```python
from django.core.management import ManagementUtility, CommandParser
import sys
import os
import traceback
import sys

def main():
    utility = ManagementUtility()
    parser = CommandParser(usage='%(prog)s subcommand [options] [args]', add_help=False, allow_abbrev=False)
    try:
        parser.parse_args(['--help'])
    except AssertionError as e:
        print_stacktrace(e)
        raise

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

if __name__ == '__main__':
    try:
        main()
    except SystemExit as e:
        if e.code != 0:
            print("Test failed", file=sys.stderr)
        else:
            print("Test passed")
```

This script creates a `ManagementUtility` instance and then attempts to parse the command-line arguments. If an `AssertionError` is raised, it prints the stack trace and re-raises the exception.