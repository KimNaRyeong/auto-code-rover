Here is the reproducer script:

```python
import django
from django.contrib import admin
from django.db import models

def main():
    class MyModel(models.Model):
        content_type_resource_contract = models.ForeignKey(
            'django.contenttypes.ContentType',
            on_delete=models.CASCADE,
            blank=True,
            null=True,
        )
        resource_contract_id = models.PositiveIntegerField(blank=True, null=True)

    class MyAdmin(admin.ModelAdmin):
        list_filter = (('content_type_resource_contract', admin.EmptyFieldListFilter),)

    try:
        MyAdmin(list_filter=MyAdmin.list_filter)
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
    django.setup()
    main()

```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.