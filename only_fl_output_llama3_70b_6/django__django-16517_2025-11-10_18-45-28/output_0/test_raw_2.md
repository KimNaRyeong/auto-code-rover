Here is the `reproducer.py` file to reproduce the issue:
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

def main():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'
    import django
    django.setup()

    from django.test.utils import setup_test_environment
    setup_test_environment()

    request_factory = RequestFactory()
    request = request_factory.get('/admin/doc/views/orders.views.OrderSearch/')

    try:
        from django.contrib.admindocs.views import ViewDetailView
        response = ViewDetailView.as_view()(request, 'orders.views.OrderSearch')
        if response.status_code == 404:
            raise AssertionError("Mixed-case views/templates names causes 404 on :view:/:template: directive.")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == '__main__':
    main()
```
This script defines a `OrderSearch` view with a doc comment that triggers the issue. It then sets up a Django test environment, creates a request for the view documentation page, and attempts to render it using `ViewDetailView`. If the response is a 404 error, it raises an `AssertionError`. If any other exception occurs, it prints the stack trace using the provided function.

To use this script, create a new Django project with a `reproducer` app, and add the following settings to your `settings.py` file:
```
INSTALLED_APPS = [
    # ...
    'reproducer',
    'django.contrib.admindocs',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            # ... some options here ...
        },
    },
]
```
Then, run the script with `python3 reproducer.py`. If the issue is present, it should raise an `AssertionError` and print a stack trace. If the issue is fixed, it should exit with code 0.