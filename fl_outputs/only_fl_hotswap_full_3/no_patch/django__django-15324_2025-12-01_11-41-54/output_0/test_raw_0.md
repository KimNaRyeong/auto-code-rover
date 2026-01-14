 Here is a standalone python script `reproducer.py` that reproduces the issue:
```python
import sys
import tempfile
from urllib.parse import urlparse

import requests
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test.client import RequestFactory

def print_stacktrace(e: Exception):
    import traceback    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def request_with_bad_filename():
    url = "http://localhost:8