Here is the reproducer script:

```python
import os
import sys
from django.core.management import execute_from_command_line
from django.core.exceptions import ImproperlyConfigured
import traceback


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
        os.chdir('/path/to/non-existent/project')
        execute_from_command_line(['django-admin.py', 'not-a-real-command', 'test'])
    except ImproperlyConfigured as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")
    else:
        assert False, "Issue should be present"


if __name__ == '__main__':
    main()
```

This script attempts to change the current directory to a non-existent project, then tries to execute the `django-admin.py` command with an unknown subcommand. If the issue is present (i.e., Django raises an `ImproperlyConfigured` exception), it prints the stack trace and raises an `AssertionError`.