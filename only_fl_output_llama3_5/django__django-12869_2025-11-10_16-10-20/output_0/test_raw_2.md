Here is the reproducer script:

```python
import os
from django.core.management import call_command
from django.conf import settings
from django.contrib.staticfiles.finders import get_finders
import sys
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
    settings.STATICFILES_DIRS = ()
    try:
        for finder in get_finders():
            finder.check()
    except Exception as e:
        raise AssertionError("Expected ImproperlyConfigured exception") from e
    print_stacktrace(e)

if __name__ == "__main__":
    main()
```

This script sets `STATICFILES_DIRS` to an empty tuple and then attempts to run the static file checks. If the expected `ImproperlyConfigured` exception is raised, it prints a stack trace and raises an `AssertionError`.