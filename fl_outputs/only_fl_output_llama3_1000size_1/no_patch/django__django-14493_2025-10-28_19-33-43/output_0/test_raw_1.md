Here is the reproducer script:

```python
import os
from django.core.management import call_command
from django.conf import settings
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage

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
    class MyManifestStaticFilesStorage(ManifestStaticFilesStorage):
        max_post_process_passes = 0

    settings.STATICFILES_STORAGE = "MyManifestStaticFilesStorage"
    try:
        call_command('collectstatic')
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

if __name__ == '__main__':
    reproduce_issue()
```

This script sets the `STATICFILES_STORAGE` setting to your custom storage class, then attempts to run the `collectstatic` command. If an exception is raised during this process, it prints the stack trace and raises an `AssertionError`.