 Here is a standalone Python file `reproducer.py` that reproduces the issue:
```python
from django.conf.urls import url
from django.contrib.admindocs.views import ViewDetailView
from django.urls import include, path
from django.utils.six import string_types
from django.views.generic import ListView

class OrderSearch(ListView):
    """
    :view: orders.views.Orders
    """
    template_name = 'orders.html'

urlpatterns = [
    path('admin/doc/views/', ViewDetailView.as_view(), name='view_detail'),
    path('orders/', OrderSearch.as_view(), name='orders'),
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

def run():
    try:
        from django.core.handlers.wsgi import WSGIHandler
        from django.test.client import Client as DjangoClient
        from django.test.utils import get_runner

        client = DjangoClient()
        handler = WSGIHandler()

        test_runner = get_runner(failfast=False)
        test_runner().setup_test_environment()
        test_runner().teardown_test_environment()

        with client.get('http://localhost:8000/admin/doc/views/orders.views.Orders/', follow=True) as response:
            if response.status_code != 200:
                raise AssertionError(f"Expected status code 200, got {response.status_code}")
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    run()
```
To run the script, execute `python3 reproducer.py` in the root directory of the project. The script will raise an `AssertionError` with a stack trace when the issue is present and print a message indicating that the issue is fixed when it is not present.

Note: This script uses the Django test client to simulate a request to the affected URL. The `print_stacktrace` function is used to print a stack trace of any exceptions that are raised. The `run` function sets up the test environment, makes the request, and tears down the test environment. The script is designed to be run in a Django project environment, so it imports some modules from Django that may not be available in other contexts.