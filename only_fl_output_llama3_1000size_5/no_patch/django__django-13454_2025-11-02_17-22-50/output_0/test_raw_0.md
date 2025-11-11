Here is the reproducer script:

```python
import django
from django.contrib import admin
from django.db import models

def main():
    class MyModel(models.Model):
        content_type_resource_contract = models.ForeignKey(
            'django.contrib.contenttypes.ContentType',
            on_delete=models.CASCADE,
            blank=True,
            null=True,
        )
        resource_contract_id = models.PositiveIntegerField(blank=True, null=True)
        resource_contract = models.GenericForeignKey('content_type_resource_contract', 'resource_contract_id')

    class MyAdmin(admin.ModelAdmin):
        list_filter = ((('resource_contract', admin.EmptyFieldListFilter),))

    try:
        admin.site.register(MyModel, MyAdmin)
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    django.setup()
    main()
```

This script sets up a simple Django project and tries to register the `MyModel` with the `MyAdmin`. If the issue is present, it will raise an `AssertionError`, which we catch and print the stack trace for.