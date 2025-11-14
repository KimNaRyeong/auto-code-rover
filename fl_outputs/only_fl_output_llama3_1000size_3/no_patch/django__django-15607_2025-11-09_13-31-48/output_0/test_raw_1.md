Here is the reproducer script:

```python
import os
import django
from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.http import HttpResponse
from django.test.client import RequestFactory
from django.core.exceptions import AssertionError

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

settings.configure(
    INSTALLED_APPS=['django.contrib.auth'],
    ROOT_URLCONF='reproducer.urls',
)

os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'

django.setup()

request_factory = RequestFactory()
view = LogoutView.as_view(next_page='/en/')

def test_reproduction():
    request = request_factory.post('/logout/?next=http://evil/', {'csrfmiddlewaretoken': 'dummy'})
    response = view(request)
    if response.status_code == 302 and len(response.redirect_chain) > 1:
        raise AssertionError("Unnecessary redirect in LogoutView when ?next=... contains 'unsafe' URL")

try:
    test_reproduction()
except AssertionError as e:
    print_stacktrace(e)

if os.path.exists('reproducer.urls.py'):
    exit(0)
else:
    exit(1)
```

This script sets up a Django environment, defines a test function that reproduces the issue, and then prints the stack trace if the test fails.