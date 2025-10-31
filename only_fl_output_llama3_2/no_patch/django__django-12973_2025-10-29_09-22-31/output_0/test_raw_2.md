Here is the reproducer script:

```python
import os
from django.conf import settings
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.exceptions import AssertionError

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
    settings.configure()
    settings.MIDDLEWARE = []
    try:
        settings.INSTALLED_APPS
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Issue fixed. Exiting with code 0.")
        exit(0)

if __name__ == "__main__":
    main()
```

This script sets the `MIDDLEWARE` setting to an empty list, then attempts to access the `INSTALLED_APPS` setting. This should raise an `ImproperlyConfigured` exception because the settings are not configured. The script prints the stack trace and exits with code 1.

To run this script, save it in a file named `reproducer.py`, then execute it using `python3 reproducer.py`.