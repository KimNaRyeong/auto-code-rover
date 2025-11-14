Here is a standalone Python script `reproducer.py` that reproduces the issue:

```python
import os
import sys
from django.core.management import execute_from_command_line

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
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ticket_30479.settings')
        execute_from_command_line(['manage.py', 'runserver'])
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    with open('manage.py', 'a') as f:
        f.write("print('sth')")
    reproduce_issue()
```

This script sets the `DJANGO_SETTINGS_MODULE` environment variable before running the management command. This should trigger the autoreloader and cause the issue to be reproduced.

To run this script, save it as `reproducer.py`, navigate to the root directory of your project, and execute it using `python3 reproducer.py`.