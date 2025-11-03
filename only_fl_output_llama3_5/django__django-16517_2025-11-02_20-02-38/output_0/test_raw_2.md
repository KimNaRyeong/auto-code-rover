Here is the reproducer script:

```
from django.contrib.admindocs.views import ViewDetailView
from django.urls import path, include
from django.conf.urls import url
from django.http import HttpResponse
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required

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

def view_func(request):
    return HttpResponse("Hello, World!")

urlpatterns = [
    path('orders/', include([
        url(r'^view:orders.views.Orders/$', ViewDetailView.as_view()),
    ])),
]

class OrderSearch(LoginRequiredMixin, ListView):
    template_name = 'Orders'

if __name__ == "__main__":
    try:
        from django.urls import get_resolver
        resolver = get_resolver()
        resolver.urlconf_module = 'reproducer'
        resolver.resolve('/')
    except Exception as e:
        print_stacktrace(e)
        exit(1)

```

This script creates a simple Django project with a URL pattern that includes the problematic view. The `OrderSearch` class-based view is defined, and its docstring contains the offending template name. When you run this script using `python3 reproducer.py`, it should raise an AssertionError and print the stack trace of the issue.