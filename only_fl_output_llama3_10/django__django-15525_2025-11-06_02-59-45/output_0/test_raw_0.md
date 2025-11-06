Here is the reproducer script:

```python
import os
import sys
from django.core.management import call_command
from django.db import IntegrityError, OperationalError
from django.test.utils import CaptureStandardOutput

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
    os.environ['DJANGO_SETTINGS_MODULE'] = 'testbug.settings'
    try:
        with CaptureStandardOutput() as capture:
            call_command('loaddata', '--database', 'other', '--format', 'json', '-')
        if "Author matching query does not exist." in capture.get_output():
            raise AssertionError("Issue reproduced")
    except (IntegrityError, OperationalError) as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script sets the `DJANGO_SETTINGS_MODULE` environment variable to point to your project's settings module. It then calls the `loaddata` management command with the specified options, capturing any output. If the expected error message is found in the captured output, an `AssertionError` is raised. If any other kind of database error occurs (e.g., due to a missing table), the script prints the stack trace and exits with code 1.