Here is the reproducer script:

```python
import os
from django.conf import settings
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware
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
    settings.MIDDLEWARE = []
    try:
        from django.contrib.auth.middleware import AuthenticationMiddleware
        from django.contrib.sessions.middleware import SessionMiddleware
        from django.contrib.messages.middleware import MessageMiddleware
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```

This script sets the `MIDDLEWARE` setting to an empty list, then attempts to import `AuthenticationMiddleware`, `SessionMiddleware`, and `MessageMiddleware`. This should raise an `AssertionError`, which is caught and printed using the provided function. The script then exits with a status code of 1.

To run this script, save it in a file named `reproducer.py` in the root directory of your project, then execute it with `python3 reproducer.py`.