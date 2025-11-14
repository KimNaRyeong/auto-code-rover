Here is a new standalone Python script `reproducer.py` to reproduce the issue:
```
# reproducer.py

import io
import requests
from django.http import HttpResponse
from django.core.wsgi import get_wsgi_application
from django.test.utils import setup_test_environment

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

def test_file_upload():
    setup_test_environment()
    
    from django.conf import settings
    settings.configure(DEBUG=True, ROOT_URLCONF='reproducer.urls')
    
    from reproducer.urls import urlpatterns
    
    application = get_wsgi_application()
    
    contents = io.StringIO("." * (1024 * 1024 * 3))
    files = {"docfile": (b"bogus.txt!", contents, "text/plain")}
    req = requests.Request("POST", "http://localhost:8000/", files=files)
    prepared = req.prepare()
    body = prepared.body
    assert isinstance(body, bytes)
    prepared.body = body.replace(b"!", b"\x00")
    
    try:
        response = application(prepared.environ, lambda s, h: None)
        assert False, "Expected ValueError to be raised"
    except ValueError as e:
        if "embedded null byte" in str(e):
            print_stacktrace(e)
            raise AssertionError("ValueError with 'embedded null byte' message")
        else:
            print_stacktrace(e)
            raise AssertionError("Expected ValueError with 'embedded null byte' message")

if __name__ == "__main__":
    test_file_upload()
```
This script sets up a minimal Django environment, defines a URL pattern for the `index` view, and then sends a request to that view with a file containing a null character in its name. If the issue is present, it should raise an `AssertionError` with a stack trace of the error.

Please create a new file `reproducer/urls.py` with the following content:
```
# reproducer/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```
And another file `reproducer/views.py` with the following content:
```
# reproducer/views.py

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django import forms

class UploadFileForm(forms.Form):
    docfile = forms.FileField()

@csrf_exempt
def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print(repr(request.FILES['docfile']))
            return HttpResponse('/')
        else:
            print("Not valid!")
            return HttpResponse('/')
    else:
        form = UploadFileForm()
    return render(request, 'uploads/index.html', {'form': form})
```
Then, run the script with `python3 reproducer.py`.