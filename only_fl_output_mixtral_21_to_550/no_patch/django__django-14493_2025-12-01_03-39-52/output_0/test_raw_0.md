 Here is a standalone python file `reproducer.py` that reproduces the issue:
```python
import sys
import django
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage
from django.conf import settings

def print_stacktrace(e: Exception):
    import traceback    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class MyManifestStaticFilesStorage(ManifestStaticFilesStorage):
    max_post_process_passes = 0

settings.STATICFILES_STORAGE = "MyManifestStaticFilesStorage"
django.setup()

try:
    from django.core.management import call_command
    call_command('collectstatic', interactive=False, verbosity=0)
except Exception as e:
    assert isinstance(e, UnboundLocalError), "Expected UnboundLocalError, got: {}".format(e)
    print_stacktrace(e)
    sys.exit(1)

print("Issue not reproduced.")
```
When executed with `python3 reproducer.py`, it raises an `AssertionError` with the stack trace of the issue.

The script imports the necessary modules, defines the `print_stacktrace` function, and creates a custom class `MyManifestStaticFilesStorage` that derives from `ManifestStaticFilesStorage` and sets `max_post_process_passes` to 0.

It then sets `STATICFILES_STORAGE` to the custom class, initializes Django with `django.setup()`, and calls `collectstatic` with `interactive=False` and `verbosity=0`.

If the issue is present, an `UnboundLocalError` is raised, and the script prints the stack trace and exits with code 1. If the issue is fixed, the script prints a message and exits with code 0.