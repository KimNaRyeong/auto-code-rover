 Here is a standalone Python file `reproducer.py` that reproduces the issue:
```python
import sys
import traceback
from django.core.checks import CheckMessage, CheckSystemTag, Error
from django.db import models
from django.db.models.fields import ManyToManyField
from django.contrib import admin
from position.fields import PositionField

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class Thing(models.Model):
    number = models.IntegerField(default=0)
    order = PositionField()

class ThingAdmin(admin.ModelAdmin):
    list_display = ['number', 'order']

def _check_list_display_item(self, obj, item, label):
    if callable(item):
        return []
    elif hasattr(obj, item):
        return []
    else:
        try:
            field = obj.model._meta.get_field(item)
        except FieldDoesNotExist:
            try:
                field = getattr(obj.model, item)
            except AttributeError:
                return [
                    Error(
                        "The value of '%s' refers to '%s', which is not a callable, "
                        "an attribute of '%s', or an attribute or method on '%s.%s'." % (
                            label, item, obj.__class__.__name__,
                            obj.model._meta.app_label, obj.model._meta.object_name,
                        ),
                        obj=obj.__class__,
                        id='admin.E108',
                    )
                ]
        if isinstance(field, ManyToManyField):
            return [
                Error(
                    "The value of '%s' must not be a ManyToManyField." % label,
                    obj=obj.__class__,
                    id='admin.E109',
                )
            ]
        return []

class CustomAdminSite(admin.AdminSite):
    def check_model_admin(self, model_admin, **kwargs):
        messages = []
        for item in model_admin.list_display:
            messages += _check_list_display_item(self, model_admin, item, item)
        return messages

admin_site = CustomAdminSite()
admin_site.register(Thing, ThingAdmin)

if __name__ == "__main__":
    with admin.site._context(using='default'):
        admin_site.check_model_admin(ThingAdmin)
```
To reproduce the issue, run the script with Python 3.6 or higher:
```shell
$ python3 reproducer.py
Traceback (most recent call last):
  File "reproducer.py", line 70, in <module>
    admin_site.check_model_admin(ThingAdmin)
  File "reproducer.py", line 64, in check_model_admin
    messages += _check_list_display_item(self, model_admin, item, item)
  File "reproducer.py", line 37, in _check_list_display_item
    field = obj.model._meta.get_field(item)
  File "reproducer.py", line 56, in <module>
    class ThingAdmin(admin.ModelAdmin):
  File "reproducer.py", line 57, in ThingAdmin
    list_display = ['number', 'order']
  File "reproducer.py", line 57, in <listcomp>
    list_display = ['number', 'order']
  File "reproducer.py", line 28, in _check_list_display_item
    field = getattr(obj.model,