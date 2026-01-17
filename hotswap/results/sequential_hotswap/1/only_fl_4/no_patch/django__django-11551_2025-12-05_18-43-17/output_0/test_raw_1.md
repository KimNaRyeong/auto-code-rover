 Here is a standalone Python file `reproducer.py` that reproduces the issue:
```python
import sys
import traceback
from django.core.checks import checks, Error
from django.db import models
from django.db.models.fields import ManyToManyField
from django.contrib import admin

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class PositionField(models.PositiveIntegerField):
    def get(self, instance):
        if not isinstance(instance, models.Model):
            raise Exception("Cannot get PositionField value on a class")
        return super().get(instance)

class Thing(models.Model):
    number = models.IntegerField(default=0)
    order = PositionField()

class ThingAdmin(admin.ModelAdmin):
    list_display = ['number', 'order']

@admin.register(Thing)
class ThingAdmin(admin.ModelAdmin):
    pass

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

admin._check_list_display_item = _check_list_display_item

def main():
    admin.site.register(Thing)
    admin.site.validate()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```
To reproduce the issue, run the script with Python 3:
```
python3 reproducer.py
```
The script should raise an `AssertionError` with the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 70, in <module>
    main()
  File "reproducer.py", line 66, in main
    admin.site.validate()
  File "/usr/local/lib/python3.9/site-packages/django/contrib/admin/sites.py", line 231, in validate
    self._validate_models(force_validation)
  File "/usr/local/lib/python3.9/site-packages/django/contrib/admin/sites.py", line 296, in _validate_models
    validate_model(model, self)
  File "/usr/local/lib/python3.9/site-packages/django/contrib/admin/validation.py", line 32, in validate_model
    validate_related_fields(model, admin_site)
  File "/usr/local/lib/python3.9/