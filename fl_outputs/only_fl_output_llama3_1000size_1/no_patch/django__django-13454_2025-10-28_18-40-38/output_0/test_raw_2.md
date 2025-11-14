Here is the reproducer script:

```python
from django.contrib import admin
from django.db import models

def main():
    try:
        class MyModel(models.Model):
            content_type = models.ForeignKey(
                'django.contenttypes.ContentType',
                on_delete=models.CASCADE,
                blank=True,
                null=True,
            )
            resource_contract_id = models.PositiveIntegerField(blank=True, null=True)
            resource_contract = models.GenericForeignKey('content_type_resource', 'resource_contract_id')

        class MyAdmin(admin.ModelAdmin):
            list_filter = ((('resource_contract'), admin.EmptyFieldListFilter),)

        admin.site.register(MyModel, MyAdmin)
    except AssertionError as e:
        print_stacktrace(e)
        raise

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
```

This script defines the model and admin class that reproduce the issue, but it does not set up a Django project. It should be executed by `python3 reproducer.py`.