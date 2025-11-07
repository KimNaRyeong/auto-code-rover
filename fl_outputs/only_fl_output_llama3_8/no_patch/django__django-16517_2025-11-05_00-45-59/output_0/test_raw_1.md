Here is the reproducer script:

```python
import os
from django.conf import settings
from django.contrib.admindocs.views import ViewDetailView
from django.core.exceptions import AssertionError
from django.urls import path, re_path
from django.views.generic import ListView

settings.configure()

class OrderSearch(LoginRequiredMixin, UserPassesTestMixin, ListView):
    pass

def view_detail(request, view_name):
    try:
        ViewDetailView._get_view_func(view_name)
    except Exception as e:
        raise AssertionError("Issue reproduced") from e

re_path(r'view:(?P<view_name>\w+)', view_detail)

if __name__ == '__main__':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
    try:
        ViewDetailView.as_view()(None, 'view:orders.views.Orders')
    except Exception as e:
        print_stacktrace(e)
        exit(1)
```

This script sets up a simple Django project with a class-based view and URL configuration. It then attempts to access the `ViewDetailView` for the given view name (`'view:orders.views.Orders'`) and prints the stack trace if an exception is raised.

To run this script, save it as `reproducer.py` in the root directory of your project and execute it with `python3 reproducer.py`. If the issue is present, you should see a 404 error page.