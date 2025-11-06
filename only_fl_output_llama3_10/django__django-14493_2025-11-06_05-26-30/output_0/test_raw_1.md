Here is the reproducer script:

```python
import os
from django.core.management import call_command
from django.conf import settings
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage
from django.utils.functional import SimpleLazyObject

def main():
    class MyManifestStaticFilesStorage(ManifestStaticFilesStorage):
        max_post_process_passes = 0

    settings.STATICFILES_STORAGE = SimpleLazyObject(lambda: MyManifestStaticFilesStorage)

    try:
        call_command('collectstatic', verbosity=0)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Error occurred while running collectstatic")

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

if __name__ == "__main__":
    main()
```

This script sets up a custom `ManifestStaticFilesStorage` class with `max_post_process_passes = 0`, and then runs the `collectstatic` command. If an error occurs, it prints the stack trace using the provided function and raises an `AssertionError`.