Here is the reproducer script:

```python
import django
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.db.models import User

def prepare_lookup_value(value):
    return value.replace(',', '')

class TestModel(admin.ModelAdmin):
    def get_queryset(self, request):
        return User.objects.all()

    def has_permission(self, request):
        return True

admin.site.register(User)

def test_prepare_lookup_value():
    try:
        admin.util.prepare_lookup_value('johnny,viola,gordon')
    except Exception as e:
        print_stacktrace(e)
        raise

test_prepare_lookup_value()
```

This script sets up a Django project and defines a simple admin model. It then attempts to call the `prepare_lookup_value` function with a value that contains a comma. If an exception is raised, it prints the stack trace and raises the same exception again.

Please note that you need to have Django installed in your Python environment for this script to run.