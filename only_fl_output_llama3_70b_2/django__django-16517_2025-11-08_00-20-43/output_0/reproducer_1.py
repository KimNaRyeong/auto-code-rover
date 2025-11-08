import os
import sys
from django.conf import settings
from django.test.utils import setup_test_environment
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import ListView
from django.test import TestCase, RequestFactory

settings.configure(
    INSTALLED_APPS=['django.contrib.admin', 'django.contrib.admindocs'],
    ROOT_URLCONF='reproducer.urls',
)

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
    setup_test_environment()
    from django.urls import path
    urlpatterns = [
        path('admin/doc/views/orders.views.Orders/', lambda request: HttpResponse()),
    ]

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
