Here is the reproducer script:

```python
import sys
from django.core.management import ManagementUtility

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

def reproduce_issue():
    try:
        utility = ManagementUtility()
        parser = CommandParser(usage='%(prog)s subcommand [options] [args]', add_help=False, allow_abbrev=False)
        raise AssertionError("Expected exception")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script creates a `ManagementUtility` instance and then tries to create a `CommandParser` with the wrong program name. The `print_stacktrace` function is used to print the stack trace of the exception.