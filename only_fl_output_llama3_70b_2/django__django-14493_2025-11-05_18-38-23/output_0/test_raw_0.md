Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
import sys
from django.conf import settings
from django.core.management import call_command
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage

class MyManifestStaticFilesStorage(ManifestStaticFilesStorage):
    max_post_process_passes = 0

settings.configure(
    STATICFILES_STORAGE='__main__.MyManifestStaticFilesStorage',
)

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

try:
    call_command('collectstatic', verbosity=0, interactive=False)
except Exception as e:
    print_stacktrace(e)
    assert isinstance(e, UnboundLocalError), "Expected UnboundLocalError"
    sys.exit(1)

sys.exit(0)
```
This script sets up a minimal Django configuration with the custom `MyManifestStaticFilesStorage` class and runs the `collectstatic` management command. If an `UnboundLocalError` exception is raised, it prints the stack trace using the provided function and exits with code 1. If no exception is raised, it exits with code 0.

To run this script, save it to a file named `reproducer.py` in the root directory of your project and execute it with `python3 reproducer.py`.