Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
import sys
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import path
from django.views.generic import ListView

class OrderSearch(ListView):
    """ :view:orders.views.Orders """
    pass

@login_required
def my_view(request):
    return HttpResponse("Hello, world!")

urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('my-view/', my_view, name='my_view'),
]

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

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reproducer.settings")
    import django
    from django.test.utils import setup_test_environment

    django.setup()
    setup_test_environment()

    try:
        from django.test.client import RequestFactory
        rf = RequestFactory()
        request = rf.get('/admin/doc/views/orders.views.Orders/')
        response = django.contrib.admindocs.views.ViewDetailView.as_view()(request, 'orders.views.Orders')
        assert response.status_code != 404, "Expected 200 OK, got 404 Not Found"
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

    sys.exit(0)
```
This script sets up a minimal Django project with an `OrderSearch` view and a URL pattern for the admin docs. It then makes a request to the `/admin/doc/views/orders.views.Orders/` URL, which should render the documentation for the `OrderSearch` view. If the response status code is 404, it raises an `AssertionError`, prints the stack trace using the provided function, and exits with code 1. If the response status code is not 404, it exits with code 0.

To run this script, save it to a file named `reproducer.py` in the root directory of your project, then execute it with `python3 reproducer.py`.