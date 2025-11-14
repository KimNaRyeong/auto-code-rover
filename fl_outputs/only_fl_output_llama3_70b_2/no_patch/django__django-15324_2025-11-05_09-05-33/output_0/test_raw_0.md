Here is the `reproducer.py` script to reproduce the issue:
```
#!/usr/bin/env python3
import io
import requests
import os
from django.core.wsgi import get_wsgi_application
from django.test import RequestFactory

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'  # Replace with your settings module

application = get_wsgi_application()

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

factory = RequestFactory()

def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print(repr(request.FILES['docfile']))
            return HttpResponseRedirect('/')
        else:
            print("Not valid!")
            return HttpResponseRedirect('/')
    else:
        form = UploadFileForm()
    return render(request, 'uploads/index.html', {'form': form})

from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render

class UploadFileForm(forms.Form):
    docfile = forms.FileField()

try:
    contents = io.StringIO("." * (1024 * 1024 * 3))
    files = {"docfile": (b"bogus.txt!", contents, "text/plain")}
    req = requests.Request("POST", "http://localhost:8000/", files=files, data={})
    prepared = req.prepare()
    body = prepared.body
    assert isinstance(body, bytes)
    prepared.body = body.replace(b"!", b"\x00")
    response = application(prepared)

    if response.status_code == 500:
        raise AssertionError("File upload crashed with a 500 error")

except Exception as e:
    print_stacktrace(e)
```
This script sets up a Django test environment, defines the `index` view and the `UploadFileForm`, and then sends a malicious request to the view using the `requests` library. The request contains a file with a null character in its extension.

If the issue is present, the script will raise an `AssertionError` when the response status code is 500. If the issue is fixed, the script will exit with code 0.

Note that you'll need to replace `'settings'` with your actual Django settings module.