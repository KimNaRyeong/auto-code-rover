Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
import sys
from django.conf import settings
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage

class MyManifestStaticFilesStorage(ManifestStaticFilesStorage):
    max_post_process_passes = 0

settings.configure(
    STATICFILES_STORAGE='MyManifestStaticFilesStorage',
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
    from django.core.management.commands.collectstatic import Command
    command = Command()
    command.handle('collectstatic', verbosity=0, interactive=False)
except Exception as e:
    print_stacktrace(e)
    assert False, "Expected no exception"
```
This script sets up a custom `STATICFILES_STORAGE` class with `max_post_process_passes` set to 0, and then runs the `collectstatic` management command. If an exception is raised during execution, it prints the stack trace using the provided function and asserts that no exception should have been raised.

To run this script, save it as `reproducer.py` in the root directory of your project and execute it with `python3 reproducer.py`.