Here is the reproducer script:

```python
import io
import requests
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.files.base import ContentFile

def index(request):
    if request.method == 'POST':
        try:
            file = request.FILES['docfile']
            temp_file = ContentFile(file.read(), name=force_text(file.name))
            temp_file.open('wb')
            temp_file.write(file.read())
            temp_file.close()
        except (ValueError, Exception) as e:
            print_stacktrace(e)
            raise
    return HttpResponse("Upload successful!")

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

def force_text(text):
    return text

if __name__ == "__main__":
    files = {"docfile": (b"bogus.txt\x00", io.BytesIO(b"." * 1024 * 1024 * 3), "text/plain")}
    req = requests.Request("POST", "http://localhost:8000/", files=files, data={})
    prepared = req.prepare()
    body = prepared.body
    assert isinstance(body, bytes)
    prepared.body = body.replace(b"!", b"\x00")
    try:
        requests.Session().send(prepared)
    except AssertionError as e:
        print_stacktrace(e)
        raise
```

This script sends a POST request to the Django view with a file that contains null bytes in its name. If the issue is present, it will raise an `AssertionError` and print the stack trace.