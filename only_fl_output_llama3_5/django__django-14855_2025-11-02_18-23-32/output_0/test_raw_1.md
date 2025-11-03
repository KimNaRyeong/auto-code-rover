Here is the reproducer script:

```python
import django
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

def main():
    try:
        django.setup()
        admin.site.register(django.contrib.auth.models.User, MyModel)
        user = django.contrib.auth.models.User()
        foreign_key = django.contrib.auth.models.Group.objects.create()
        user.foreign_key = foreign_key
        get_admin_url(foreign_key, MyModel())
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    main()
```

This script should be run in a Django project environment.