 I apologize for the error in my previous response. Here is a corrected version of the `reproducer.py` file that should reproduce the issue:
```python
from django.conf.urls import url
from django.contrib.admindocs.views import ViewDetailView
from django.urls import include, path
from django.utils.six import string_types

class OrderSearch(ViewDetailView):
    pass

urlpatterns = [
    url(r'^views/orders/(?P<namespace>[-\w]+)/(?P<view_name>[-\w]+)/$', OrderSearch.as_view(), name='view-detail'),
]

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_issue():
    request = None
    view_name = "orders.views.Orders"
    try:
        if not isinstance(view_name, string_types):
            raise TypeError("view_name must be a string")
        view_func = ViewDetailView._get_view_func(view_name)
        assert view_func is not None, "view_func should not be None"
    except AssertionError as e:
        print_stacktrace(e)
        raise
    except Exception as e:
        print_stacktrace(e)
        assert False, "Unexpected exception"

if __name__ == "__main__":
    test_issue()
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` and print a stack trace showing the line where the issue is present.

The issue is caused by the `_get_view_func` method in `django.contrib.admindocs.views` which converts the view name to lowercase before resolving it to a view function. In this case, the view name `orders.views.Orders` is converted to `orders.views.orders`, which does not match the expected URL pattern and results in a 404 error.

To fix the issue, you can either modify the `_get_view_func` method to preserve the case of the view name, or use all lowercase view names in your documentation.

I hope this version works correctly. Let me know if you have any further issues.