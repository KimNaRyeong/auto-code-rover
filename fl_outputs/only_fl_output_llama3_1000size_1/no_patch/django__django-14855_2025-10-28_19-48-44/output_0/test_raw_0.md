Here is the reproducer script:

```python
import os
from django.contrib import admin
from django.urls import reverse
from django.test.utils import override_settings

def get_admin_url(remote_obj, model_admin):
    url_name = 'admin:%s_%s_change' % (remote_obj._meta.app_label, remote_obj._meta.model_name)
    return reverse(url_name, args=[quote(remote_obj.pk)])

class MyModel(admin.ModelAdmin):
    readonly_fields = ['foreign_key']

class MyAdminSite(admin.AdminSite):
    def has_permission(self, request):
        return True

admin.site.register(MyModel, MyModel)

@override_settings(ROOT_URLCONF='myproject.urls')
def reproduce_issue():
    try:
        obj = MyModel()
        obj.foreign_key = 1
        url = get_admin_url(obj, MyModel())
        print(f"URL: {url}")
    except AssertionError as e:
        print_stacktrace(e)
        os._exit(0)

reproduce_issue()
```

This script creates a custom admin site and model with a readonly field. It then calls the `get_admin_url` function to generate the URL for the readonly field, which should raise an `AssertionError` when the issue is present.

The script uses the `print_stacktrace` function to print the stack trace of the exception, and exits with code 0 when the issue is fixed.