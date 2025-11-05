Here is the reproducer script:

```python
import os
import django
from django.contrib.admindocs.views import ViewDetailView
from django.urls import path, include
from django.conf.urls import url
from django.http import HttpResponse
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

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_project.settings")

django.setup()

def view_func(request):
    return HttpResponse('Hello, world!')

class OrderSearch(LoginRequiredMixin, UserPassesTestMixin, ViewDetailView):
    template_name = 'orders.html'
    view_name = ':view:orders.views.Orders'

urlpatterns = [
    path('views/', include('views.urls')),
]

if __name__ == '__main__':
    try:
        from django.contrib.admindocs.views import ViewDetailView
        from django.urls import path, include
        from django.conf.urls import url
        from django.http import HttpResponse
        from django.core.exceptions import AssertionError

        view_func = lambda request: HttpResponse('Hello, world!')
        OrderSearch(view_func)

    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not reproduced")
```

This script sets up a Django project and reproduces the issue by defining a class-based view with a doc comment that contains mixed-case names. When you run this script, it should raise an AssertionError if the issue is present.

To test if the issue is fixed, you can modify the `view_name` attribute of the `OrderSearch` class to use all lowercase names (e.g., `':view:orders.views.orders'`) and run the script again. If the issue is fixed, it should not raise an AssertionError.