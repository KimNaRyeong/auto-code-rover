Here is the reproducer script:

```python
import django
from django.urls import path
from django.views.generic.base import View

def main():
    urlpatterns = [
        path('home', HomeView),
    ]

    try:
        django.setup()
        django.urls.get_resolver().urlconf_module
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected error")

class HomeView(View):
    pass

if __name__ == "__main__":
    main()
```

This script sets up a Django project, defines an empty CBV, and then tries to get the resolver's URL configuration. This should reproduce the issue when run with `python3 reproducer.py`.