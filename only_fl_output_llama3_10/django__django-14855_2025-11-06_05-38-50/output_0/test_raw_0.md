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

class MyModelAdmin(admin.ModelAdmin):
    pass

@override_settings(ROOT_URLCONF='myproject.urls')
def reproduce_issue():
    admin.site.register(MyModel, model_admin=MyModelAdmin)
    my_model = MyModel()
    my_model.foreign_key = MyModel()
    url = get_admin_url(MyModelAdmin, my_model.foreign_key)
    assert url.startswith('/custom-admin/'), "URL should start with '/custom-admin/'"
    raise AssertionError("Issue not reproduced")

if __name__ == '__main__':
    try:
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```

This script creates a custom admin site, registers the model, and then tries to generate the URL for the readonly field. If the issue is present (i.e., the URL does not start with '/custom-admin/'), it raises an `AssertionError` and prints the stack trace using the provided function.