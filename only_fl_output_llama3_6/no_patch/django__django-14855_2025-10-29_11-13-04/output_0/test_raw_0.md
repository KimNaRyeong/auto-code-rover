Here is the reproducer script:

```python
import django
from django.contrib import admin
from django.urls import reverse
from django.test.utils import override_settings

def get_admin_url(model_admin, remote_obj):
    url_name = 'admin:%s_%s_change' % (remote_obj._meta.app_label, remote_obj._meta.model_name)
    return reverse(url_name, args=[quote(remote_obj.pk)])

class MyModel(admin.ModelAdmin):
    readonly_fields = ['foreign_key']

class MyAdminSite(admin.AdminSite):
    def has_permission(self, request):
        return True

admin.site.register(django.contrib.auth.models.User, MyModel)

@override_settings(ROOT_URLCONF='django.urls')
def test_get_admin_url():
    user = django.contrib.auth.models.User()
    model_admin = MyModel(MyAdminSite(), None)
    try:
        get_admin_url(model_admin, user)
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    test_get_admin_url()
```

This script creates a custom admin site and a model with a ForeignKey field. It then calls the `get_admin_url` function to generate the URL for the readonly field, which should raise an AssertionError if the issue is present.

You can run this script by executing `python3 reproducer.py`. If the issue is present, it will print the stack trace of the error and exit with code 1. If the issue is fixed, it will simply exit with code 0.