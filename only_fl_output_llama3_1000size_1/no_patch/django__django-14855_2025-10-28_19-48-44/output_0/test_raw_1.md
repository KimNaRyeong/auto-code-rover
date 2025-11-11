Here is a revised version of the reproducer script:

```python
import os
from django.contrib import admin
from django.urls import reverse, quote
from django.test.utils import override_settings

def get_admin_url(remote_obj, model_admin):
    url_name = 'admin:%s_%s_change' % (remote_obj._meta.app_label, remote_obj._meta.model_name)
    return reverse(url_name, args=[quote(remote_obj.pk)], current_app=model_admin.admin_site.name)

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

This script should reproduce the issue by calling `get_admin_url` with a readonly field in a custom admin site.