 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import os
import shutil
from django.core.files.uploadhandler import TemporaryFileUploadHandler
from django.core.exceptions import SuspiciousOperation

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

# Settings
MEDIA_ROOT = 'media/'
FILE_UPLOAD_MAX_MEMORY_SIZE = 102