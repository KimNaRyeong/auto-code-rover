Here is the reproducer script:

```python
import requests
from django.http import HttpResponse, HttpRequest
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.views.decorators.csrf import csrf_exempt

def reproduce_issue():
    contents = io.StringIO("." * (1024 * 1024 * 3))
    files = {"docfile": (b"bogus.txt\x00!", contents, "text/plain")}
    req = HttpRequest()
    req.method = 'POST'
    req.FILES = {'docfile': InMemoryUploadedFile(io.BytesIO(b"bogus.txt\x00!"), None, "bogus.txt", 1024*3+7, "text/plain", None)}
    req.POST = {}
    
    try:
        index(request=req)
    except Exception as e:
        print_stacktrace(e)
        raise

def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print(repr(request.FILES['docfile']))
            return HttpResponse("Success")
        else:
            print("Not valid!")
            return HttpResponse("Failed")
    else:
        form = UploadFileForm()
        return render(request, 'uploads/index.html', {'form': form})

if __name__ == "__main__":
    reproduce_issue()

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

```

This script creates a POST request with a file that has a null byte in its name, then calls the `index` function to simulate the upload. If an exception is raised during this process, it prints the stack trace and raises the exception again.