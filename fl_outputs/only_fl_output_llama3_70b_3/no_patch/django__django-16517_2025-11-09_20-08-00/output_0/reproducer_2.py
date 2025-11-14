import os
import sys
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import ListView
from django.test import TestCase, RequestFactory

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

# Create the view
class OrderSearch(ListView):
    """ :view:orders.views.Orders """
    pass

try:
    # Run the development server
    os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer_project.settings'
    import reproducer_project.settings
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'runserver'])

    factory = RequestFactory()
    request = factory.get('/admin/doc/views/orders.views.Orders/')
    response = login_required(OrderSearch.as_view())(request)
    assert response.status_code != 404, "Expected 200 OK, got 404 Not Found"
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue is present") from e
