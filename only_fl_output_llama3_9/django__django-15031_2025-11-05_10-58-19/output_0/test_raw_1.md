Here is the reproducer script:

```python
import django
from django.contrib import admin
from django.contrib.auth.models import User

def prepare_lookup_value(value):
    if value.startswith('[') and value.endswith(']'):
        return [x.strip() for x in value[1:-1].split(',')]
    elif ',' in value:
        raise AssertionError("Comma not allowed")
    else:
        return [value]

class TestModel(admin.ModelAdmin):
    def get_queryset(self, request):
        users = User.objects.all()
        return users

admin.site.register(User, TestModel)

def test_issue():
    try:
        admin.ModelAdmin.prepare_lookup_value('johnny,viola,gordon')
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

test_issue()
```

This script creates a Django admin model and tries to filter the queryset using the `prepare_lookup_value` function. If the issue is present (i.e., an `AssertionError` is raised), it prints the stack trace and exits with code 1.

Please note that this script should be executed in the root directory of your project, where you have a valid Django settings file (`settings.py`).