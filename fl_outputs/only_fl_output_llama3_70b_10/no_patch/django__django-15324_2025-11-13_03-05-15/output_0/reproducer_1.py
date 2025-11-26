#!/usr/bin/env python3

import os
import sys
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse, HttpRequest
from django.test.client import RequestFactory

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

def test_upload_file():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    from django.conf import settings
    settings.configure()

    from django.http import HttpResponse
    from django.views.decorators.csrf import csrf_exempt

    @csrf_exempt
    def index(request):
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                print(repr(request.FILES['docfile']))
                return HttpResponse('OK')
            else:
                print("Not valid!")
                return HttpResponse('Not valid!')
        else:
            form = UploadFileForm()
            return HttpResponse('Form')

    from django import forms

    class UploadFileForm(forms.Form):
        docfile = forms.FileField()

    factory = RequestFactory()

    contents = b'.' * (1024 * 1024 * 3)
    files = {"docfile": (b"bogus.txt\x00", contents, "text/plain")}
    request = factory.request(method='POST', FILES=files)

    try:
        response = index(request)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue is present")

if __name__ == "__main__":
    test_upload_file()
