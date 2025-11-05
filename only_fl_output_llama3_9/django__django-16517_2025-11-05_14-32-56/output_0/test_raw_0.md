Here is the reproducer script:

```python
import os
import django
from django.contrib.admindocs.views import ViewDetailView
from django.urls import path, include
from django.conf.urls import url
from django.http import HttpResponse

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_project.settings")

django.setup()

urlpatterns = [
    path('views/', include('views.urls')),
]

def view_func(request):
    return HttpResponse('Hello, world!')

class OrderSearch(ViewDetailView):
    template_name = 'orders.html'
    view_name = ':view:orders.views.Orders'

urlpatterns.append(url(r'orders.views.orders/$', ViewDetailView.as_view(view_func)))

if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'runserver'])
```

This script sets up a Django project and reproduces the issue by defining a class-based view with a doc comment that contains mixed-case names. When you run this script, it starts a development server and you can access the view by visiting `http://localhost:8000/admin/doc/views/orders.views.orders/` in your web browser. This should raise a 404 error.

To test if the issue is fixed, you can modify the `view_name` attribute of the `OrderSearch` class to use all lowercase names (e.g., `':view:orders.views.orders'`) and run the script again. If the issue is fixed, it should not raise an AssertionError.