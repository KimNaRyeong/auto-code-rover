Here is the `reproducer.py` file to reproduce the issue:
```
import os
import sys
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import ListView
from django.test import TestCase, RequestFactory

class OrderSearch(ListView):
    """ :view:orders.views.Orders """
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

def main():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'
    import django
    django.setup()

    from django.test.utils import setup_test_environment
    setup_test_environment()

    request_factory = RequestFactory()
    request = request_factory.get('/admin/doc/views/orders.views.Orders/')

    try:
        from django.contrib.admindocs.views import ViewDetailView
        response = ViewDetailView.as_view()(request, 'orders.views.Orders')
        assert response.status_code != 404, "Expected 200 OK, got 404 Not Found"
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue is present")

if __name__ == '__main__':
    main()
```
This script defines a `ListView` with a doc comment that triggers the issue. It then sets up a Django test environment and makes a request to the URL that should render the view documentation. If the response status code is 404, it raises an `AssertionError` with a stack trace of the exception.

To use this script, create a new Django project and add a `reproducer` app to it. Create a `settings.py` file in the `reproducer` directory with the following content:
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.admindocs',
    'reproducer',
]
```
<|start_header_id|>