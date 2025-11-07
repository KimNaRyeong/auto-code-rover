Here is the reproducer script:

```python
import requests
from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.uploadhandler import TemporaryUploadedFile

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
    settings.MEDIA_ROOT = '/tmp'
    settings.MEDIA_URL = '/media/'
    
    request = HttpRequest()
    request.method = 'POST'
    request.FILES = {'docfile': TemporaryUploadedFile('bogus.txt\x00.txt', ContentFile(b''), 'text/plain')}
    request.POST = {}
    
    from . import views
    response = views.index(request)
    
    if isinstance(response, HttpResponse):
        print("Issue reproduced")
    else:
        raise AssertionError("Issue not reproduced")

try:
    reproduce_issue()
except Exception as e:
    print_stacktrace(e)
    exit(1)

print("Issue fixed")
exit(0)
```

This script sets up a test request with a file upload containing null characters in the filename, then calls the `index` view function to see if it raises an exception. If it does, it prints the stack trace and exits with code 1; otherwise, it prints "Issue fixed" and exits with code 0.