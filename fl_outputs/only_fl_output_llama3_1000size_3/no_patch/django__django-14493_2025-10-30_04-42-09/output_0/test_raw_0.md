Here is the reproducer script:

```python
import os
from django.core.management import call_command
from django.conf import settings
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage
from unittest.mock import patch, mock_open
from io import StringIO
import sys
import traceback
import sys

def print_stacktrace(e: Exception):
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

    with patch('builtins.open', new=mock_open()) as mock_file:
        with patch('django.core.files.base.ContentFile') as mock_contentfile:
            with patch('io.StringIO') as mock_stringio:
                try:
                    call_command('collectstatic')
                except Exception as e:
                    print_stacktrace(e)
                    raise AssertionError("Issue not fixed")

    if os.path.exists('static'):
        os.rmdir('static')

if __name__ == "__main__":
    reproduce_issue()
```

This script sets up a custom `MyManifestStaticFilesStorage` class with `max_post_process_passes = 0`, then runs the `collectstatic` command. If an error occurs, it prints the stack trace and raises an `AssertionError`.