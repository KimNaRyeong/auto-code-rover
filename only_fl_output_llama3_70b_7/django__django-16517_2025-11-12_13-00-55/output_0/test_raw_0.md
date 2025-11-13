Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
import sys
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import ListView
from django.test import TestCase, RequestFactory

class OrderSearch(ListView):
    """ :view:orders.views.OrderSearch """
    pass

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

os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'

import reproducer.settings

from django.core.management import execute_from_command_line
execute_from_command_line(['', 'runserver'])

factory = RequestFactory()

request = factory.get('/admin/doc/views/orders.views.OrderSearch/')
try:
    response = login_required(OrderSearch.as_view())(request)
    assert response.status_code != 404, "Expected 200 OK, got 404 Not Found"
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue is present") from e
```
This script defines a `OrderSearch` view with a doc comment that triggers the issue. It then starts a Django development server and makes a request to the view using the `RequestFactory`. If the response status code is 404, it raises an `AssertionError` with a stack trace of the exception.

To use this script, create a new Django project with `django-admin startproject reproducer`, then add the `reproducer.py` file to the root directory of the project. Run the script with `python3 reproducer.py`. If the issue is present, it should raise an `AssertionError` and print a stack trace. If the issue is fixed, it should exit with code 0.