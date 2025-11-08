Here is the reproducer script:

```python
import os
import sys
from django.core.management import execute_from_command_line
from unittest.mock import patch

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
    with patch('django.utils.autoreload.reloader') as reloader_mock:
        reloader_mock.return_value.run = MagicMock(return_value=None)
        execute_from_command_line(['manage.py', 'runserver'])

    # Make some changes to manage.py
    with open('manage.py', 'a') as f:
        f.write('\nprint("hello")')

    try:
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == '__main__':
    reproduce_issue()
```

This script will run the Django development server, make some changes to `manage.py`, and then check if an `AssertionError` is raised. If it is, it will print the stack trace and exit with code 1.