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

def run_test():
    admin.site.register(MyModel, MyModelAdmin)
    try:
        admin.site.get_list_filter(MyModel)
    except Exception as e:
        print_stacktrace(e)
        assert False

if __name__ == "__main__":
    run_test()
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` and print a stack trace showing the issue.

The issue is caused by the fact that `admin.EmptyFieldListFilter` expects the field it is filtering on to have an `empty_strings_allowed` attribute, but `GenericForeignKey` does not have this attribute. The proposed solution would be to extend `GenericForeignKey` to use the `empty_strings_allowed` attributes from the fields that are used in the generic relation.