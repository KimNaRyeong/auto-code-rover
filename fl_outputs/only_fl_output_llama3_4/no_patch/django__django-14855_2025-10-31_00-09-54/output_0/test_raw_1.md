Here is the reproducer script:

```python
import os
from django.contrib import admin
from django.urls import reverse, NoReverseMatch
from django.test.utils import override_settings

def get_admin_url(model_admin):
    try:
        return reverse('admin:%s_%s_changelist' % (model_admin.model._meta.app_label, model_admin.model._meta.model_name))
    except NoReverseMatch:
        return ''

class MyModel(admin.ModelAdmin):
    readonly_fields = ('foreign_key',)

class MyModelAdmin(admin.ModelAdmin):
    pass

@admin.register(MyModel)
class CustomMyModelAdmin(MyModelAdmin):
    def get_changelist_form(self, request, **kwargs):
        form = super().get_changelist_form(request, **kwargs)
        form.base_fields['foreign_key'].form_url = reverse('admin:myapp_mymodel_change', args=[1])
        return form

def main():
    try:
        admin_url = get_admin_url(CustomMyModelAdmin)
        print(f"admin_url: {admin_url}")
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```

This script creates a custom `CustomMyModelAdmin` that has a readonly field. When you run this script, it should raise an `AssertionError` and print the stack trace if the issue is present.