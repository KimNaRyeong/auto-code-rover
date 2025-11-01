import os
import django
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.conf import settings

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
    os.environ['DJANGO_SETTINGS_MODULE'] = 'app.settings'
    try:
        django.setup()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("CSRF failure incorrectly reported on upload when there is a problem with storage")

if __name__ == "__main__":
    reproduce_issue()
