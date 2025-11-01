Here is the reproducer script:

```python
import os
from django.contrib.admindocs.views import ViewDetailView
from django.urls import path, include
from django.urls.resolvers import URLPattern
from django.conf.urls import url
from django.http import Http404
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

def main():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'test_project.settings'

    from django.conf import settings
    from django.core.wsgi import get_wsgi_application

    application = get_wsgi_application()

    urlpatterns = [
        path('admin/doc/', include('django.contrib.admindocs.urls')),
        url(r'^orders/$', ViewDetailView.as_view(view='view:orders.views.Orders'), name='orders'),
    ]

    settings.configure(
        INSTALLED_APPS=['test_project'],
        ROOT_URLCONF='reproducer',
        URLPATTERNS=urlpatterns,
    )

    try:
        from django.contrib.admindocs.views import view_detail
        view_detail('view:orders.views.Orders')
    except Http404 as e:
        print_stacktrace(e)
        raise AssertionError("Expected 404 not found")
    else:
        print("Issue is fixed, exiting with code 0")
        exit(0)

if __name__ == "__main__":
    main()
```

This script sets up a minimal Django project and attempts to access the view 'view:orders.views.Orders' using the `ViewDetailView`. If it raises a 404 error, it prints the stack trace and raises an assertion error.