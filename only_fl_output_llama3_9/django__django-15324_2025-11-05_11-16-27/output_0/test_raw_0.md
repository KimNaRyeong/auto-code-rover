Here is the reproducer script:

```python
import requests
from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import ValidationError

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

def reproducer():
    settings.MEDIA_ROOT = '.'
    settings.MEDIA_URL = '/media/'
    
    contents = io.StringIO("." * (1024 * 1024 * 3))
    files = {"docfile": (b"bogus.txt!", contents, "text/plain")}
    req = requests.Request("POST", "/upload/", files=files)
    prepared = req.prepare()
    body = prepared.body
    assert isinstance(body, bytes)
    prepared.body = body.replace(b"!", b"\x00")
    
    try:
        session = requests.Session()
        response = session.send(prepared)
        if response.status_code != 200:
            print_stacktrace(response.exceptions[0])
            raise AssertionError("Failed to reproduce the issue")
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    reproducer()
```

This script will attempt to upload a file with a null byte in its name and check if it raises an exception. If it does, it will print the stack trace and raise an AssertionError.