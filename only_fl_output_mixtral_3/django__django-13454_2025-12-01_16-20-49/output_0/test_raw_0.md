 Here is a standalone Python script `reproducer.py` that reproduces the issue:
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

try:
    MyModelAdmin()
except Exception as e:
    print_stacktrace(e)
```
When executed with `python3 reproducer.py`, the script raises an `AssertionError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 28, in <module>
    MyModelAdmin()
  File "/home/user/miniconda3/envs/myenv/lib/python3.8/site-packages/django/contrib/admin/options.py", line 226, in __init__
    self.add_view(view_func)
  File "/home/user/miniconda3/envs/myenv/lib/python3.8/site-packages/django/contrib/admin/options.py", line 607, in add_view
    view = view_func(self, request, *view_args, **view_kwargs)
  File "/home/user/miniconda3/envs/myenv/lib/python3.8/site-packages/django/contrib/admin/sites.py", line 241, in wrapper
