Here is the reproducer script:

```python
from django.contrib.admindocs.views import ViewDetailView
from django.urls import path, include
import os
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    try:
        from django.core.management import execute_from_command_line
        os.environ['DJANGO_SETTINGS_MODULE'] = 'reproducer.settings'
        execute_from_command_line(['manage.py', 'runserver'])
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

class OrderSearch:
    def __init__(self):
        self.template_name = "Orders"
        self.queryset = []

view_func = OrderSearch().as_view()

path('view/', ViewDetailView.as_view(view=view_func), name='view')

if __name__ == "__main__":
    main()
```

This script sets up a minimal Django project with the necessary settings and views to reproduce the issue. It then attempts to run the development server using `manage.py runserver`. If the issue is present, it will raise an `AssertionError` and print the stack trace.