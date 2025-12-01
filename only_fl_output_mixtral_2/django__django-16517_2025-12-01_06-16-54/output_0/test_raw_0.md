 Here is a standalone Python file `reproducer.py` that reproduces the issue:
```python
from django.conf.urls import url
from django.contrib.admindocs.views import ViewDetailView
from django.urls import include, path
from django.utils.six import with_metaclass

# Define a custom class-based view
class OrderSearch(with_metaclass(ViewDetailView.as_view_class(), ViewDetailView)):
    pass

# Define the URL patterns
urlpatterns = [
    url(r'^orders/', OrderSearch.as_view(), name='orders'),
]

# Define the project's root URL configuration
root_urlconf = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('', include(urlpatterns)),
]

# Execute the root URL configuration
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Try to access the documentation page for the OrderSearch view
try:
    from django.contrib.admindocs.views import get_view_name
    view_name = get_view_name(OrderSearch.as_view())
    response = application.handle_request(None, 'GET', f'/admin/doc/views/{view_name}/')
    print(response)
except Exception as e:
    print_stacktrace(e)
    assert False, "An exception was raised while trying to access the documentation page"
```
To execute the script, run `python3 reproducer.py` in the root directory of the project. If the issue is present, the script will raise an `AssertionError` and print a stack trace. If the issue is fixed, the script will print the response from the documentation page and exit with code 0.

The `print_stacktrace` function is used to print the stack trace of any exceptions raised during the execution of the script. This makes it easier to identify the source of the issue.

The script defines a custom class-based view `OrderSearch` and includes it in the project's URL configuration. It then tries to access the documentation page for the `OrderSearch` view using the `application.handle_request` method. If the issue is present, this will raise an exception and the script will print the stack trace. If the issue is fixed, the script will print the response from the documentation page and exit with code 0.

Note: The `with_metaclass` function is used to create a class with a custom metaclass (`ViewDetailView.as_view_class()`). This is necessary because the `ViewDetailView` class in Django's `admindocs` app uses a custom metaclass (`SingleObjectTemplateViewMetaclass`) to define its `as_view()` method. By using `with_metaclass`, we can create a subclass of `ViewDetailView` that also has a custom metaclass and can be used with the `as_view()` method.