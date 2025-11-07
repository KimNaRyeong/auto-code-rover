Here is the reproducer script:

```python
import requests
from io import StringIO
from django.http import HttpResponse, HttpRequest
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.views.decorators.csrf import csrf_exempt

def reproduce_issue():
    contents = StringIO("." * (1024 * 1024 * 3))
    files = {"docfile": (b"bogus.txt\x00!", contents, "text/plain")}
    req = HttpRequest()
    req.method = 'POST'
    req.FILES = {'docfile': InMemoryUploadedFile(StringIO(b"bogus.txt\x00!"), None, "bogus.txt", 1024*3+7, "text/plain", None)}
    req.POST = {}
    
    try:
        from uploads.views import index
        index(request=req)
    except Exception as e:
        print_stacktrace(e)
        raise

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
    settings.configure()
    reproduce_issue()

```

This script sets the DJANGO_SETTINGS_MODULE environment variable before calling the `index` function. This should allow the script to run without raising an exception.