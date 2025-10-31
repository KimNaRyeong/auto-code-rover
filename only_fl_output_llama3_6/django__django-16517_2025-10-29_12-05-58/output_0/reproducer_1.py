import os
from django.contrib.admindocs.views import ViewDetailView
from django.http import Http404
from django.urls import path, re_path
from django.views.generic import ListView
from django.conf import settings
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

def reproducer():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'test_project.settings'
    from django.conf import settings
    settings.configure()

    class OrderSearch(ListView):
        def get(self, request):
            return Http404('Page not found')

        def as_view(cls):
            view_func = cls.as_view()
            view_func.__name__ = f"Orders"
            return view_func

    view_func = OrderSearch().as_view()
    path_info = '/orders/views/Orders/'
    try:
        ViewDetailView(view_func).dispatch({'PATH_INFO': re_path(path_info)}, None)
    except Http404 as e:
        print_stacktrace(e)
    else:
        assert False, "Expected 404 error"

if __name__ == '__main__':
    reproducer()
