Here is the reproducer script:

```python
import os
from django.core.management import execute_from_command_line
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

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
    try:
        os.chdir('/path/to/non-existent/django/project')
        settings.configure()
        execute_from_command_line(['django-admin.py', 'not-a-real-command', 'test'])
    except ImproperlyConfigured as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")
    else:
        assert False, "Expected ImproperlyConfigured exception"

if __name__ == '__main__':
    main()
```

This script attempts to run the `django-admin` command in a non-existent Django project. If the issue is present, it will raise an `AssertionError`.