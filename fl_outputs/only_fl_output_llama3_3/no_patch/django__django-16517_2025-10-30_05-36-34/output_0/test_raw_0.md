Here is the reproducer script:

```python
import os
from django.contrib.admindocs.views import ViewDetailView
from django.urls import path
from django.views.generic import ListView
from django.conf import settings

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
    settings.configure()
    os.environ['DJANGO_SETTINGS_MODULE'] = 'test_project.settings'

    class OrderSearch(ListView):
        template_name = "orders.html"
        queryset = []

    view_func = OrderSearch.as_view()

    path('orders/', include('orders.urls'))
    path('orders/view/', ViewDetailView.as_view(view=view_func), name='view')

    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'runserver'])
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```

This script sets up a minimal Django project with the necessary settings and views to reproduce the issue. It then attempts to run the development server using `manage.py runserver`. If the issue is present, it will raise an `AssertionError` and print the stack trace.