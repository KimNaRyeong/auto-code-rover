Here is the reproducer.py script:
```
import os
from django.test.utils import setup_test_environment
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import connection

os.environ['DJANGO_SETTINGS_MODULE'] = 'your_project.settings'  # Replace with your project's settings module

setup_test_environment()

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

try:
    url = reverse('admin:auth_user_changelist')
    response = client.get(url, {'q': '\x00'})  # %00 is the null character
    assert response.status_code != 500, "Admin search with a null character crashes"
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Admin search with a null character crashes")

print("Issue not present")
```
This script sets up a test environment for Django, defines a function to print the stack trace of an exception, and then tries to reproduce the issue by making a GET request to the admin user changelist view with a query parameter containing a null character. If the response status code is 500 (indicating an internal server error), it prints the stack trace of the exception and raises an AssertionError. If the response status code is not 500, it prints "Issue not present" and exits with code 0.

Note that you should replace `'your_project.settings'` with your project's settings module.