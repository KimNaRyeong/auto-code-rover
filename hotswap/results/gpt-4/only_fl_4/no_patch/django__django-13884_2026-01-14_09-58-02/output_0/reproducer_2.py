# reproducer.py

import sys
from django.conf import settings
from django.core.handlers.wsgi import WSGIHandler
from django.http import HttpResponse
from django.urls import path
from urllib.parse import quote, unquote

# Define a minimal Django application
settings.configure(
    SECRET_KEY='a-secret-key',
    ROOT_URLCONF=__name__,
)

def set_language(request):
    next_url = request.POST.get('next', '/')
    # Simulate redirect to unquoted URL
    response = HttpResponse(status=302)
    response['Location'] = unquote(next_url)
    return response

urlpatterns = [
    path('set_language/', set_language, name='set_language'),
]

# Django setup
from django.core.management import execute_from_command_line
import django
django.setup()

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_set_language_url_params():
    from django.test import Client
    client = Client()
    # URL with parameter value including encoded '&'
    next_url = '/?parameter=some%20%26%20thing'
    try:
        response = client.post('/set_language/', {'next': next_url})
        assert unquote(response['Location']) == next_url, "The URL was incorrectly unquoted"
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        print("Test passed: The URL was correctly handled.")
        sys.exit(0)

if __name__ == '__main__':
    test_set_language_url_params()
