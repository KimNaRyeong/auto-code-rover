Here is the standalone Python script `reproducer.py` to reproduce the issue:
```
import os
import io
from django.core.management import setup_environ
from django.http import HttpResponseServerError
from django.test.client import RequestFactory
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

def reproduce_issue():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    setup_environ()
    setup_test_environment()

    from django import forms
    from django.http import HttpResponseRedirect
    from django.shortcuts import render
    from django.views.decorators.csrf import csrf_exempt

    class UploadFileForm(forms.Form):
        docfile = forms.FileField()

    @csrf_exempt
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

    factory = RequestFactory()

    contents = io.StringIO("." * (1024 * 1024 * 3))
    files = {"docfile": (b"bogus.txt\x00", contents, "text/plain")}
    request = factory.post('/', data={}, files=files)

    try:
        index(request)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue is present.")

if __name__ == "__main__":
    reproduce_issue()
```
This script sets up a Django test environment, defines an upload form and view, and then sends a POST request with a file that has a null byte in its filename. If the issue is present, it should raise an `AssertionError` with a stack trace of the error.