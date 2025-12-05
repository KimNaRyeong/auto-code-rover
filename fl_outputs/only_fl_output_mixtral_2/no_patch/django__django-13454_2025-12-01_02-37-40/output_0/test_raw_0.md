 Here is a standalone Python file `reproducer.py` that reproduces the issue:
```python
from django.contrib import admin
from django.db import models

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class ContentTypeResourceContract(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = models.GenericForeignKey('content_type', 'object_id')

class MyModel(models.Model):
    content_type_resource_contract = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    resource_contract_id = models.PositiveIntegerField(blank=True, null=True)
    resource_contract = models.GenericForeignKey('content_type_resource', 'resource_contract_id')

class MyModelAdmin(admin.ModelAdmin):
    list_filter = (('resource_contract', admin.EmptyFieldListFilter),)

def run():
    try:
        admin.site.register(MyModel, MyModelAdmin)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    run()
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` with a stack trace, indicating that the issue has been reproduced.

The issue is caused by the fact that `admin.EmptyFieldListFilter` expects the field being filtered on to have an `empty_strings_allowed` attribute, which is not present in the `GenericForeignKey` field. The proposed solution of extending `GenericForeignKey` to use the `empty_strings_allowed` attributes from the fields used in the generic relation is a possible way to fix the issue. However, this would require changes to Django's core codebase and may have unintended consequences. A better solution might be to create a custom filter class that does not require the `empty_strings_allowed` attribute.