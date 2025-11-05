Here is the reproducer script:

```python
import os
from django.contrib import admin
from django.urls import reverse, NoReverseMatch
from django.test.utils import setup_test_environment
setup_test_environment()

class ParentModel(admin.ModelAdmin):
    def get_admin_url(self, obj):
        try:
            return reverse('admin:myapp_parent_change', args=[obj.pk])
        except NoReverseMatch as e:
            print_stacktrace(e)
            raise AssertionError("Failed to generate URL")

class ChildModel(admin.ModelAdmin):
    readonly_fields = ['parent']
    list_display = ('name', 'parent')

    def get_parent(self, obj):
        return obj.parent

admin.site.register(ChildModel, ChildModelAdmin)

def main():
    try:
        child_model_admin = ChildModelAdmin()
        parent_obj = ParentModel()
        url = child_model_admin.get_admin_url(parent_obj)
        print(f"Generated URL: {url}")
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()

```

This script should be run from the root directory of your project.