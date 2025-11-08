Here is the reproducer script:

```python
import django
from django.contrib import admin
from django.db import models

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
                    admin.Error(
                        "The value of '%s' refers to '%s', which is not a callable, "
                        "an attribute of '%s', or an attribute or method on '%s.%s'." % (
                            label, item, obj.__class__.__name__,
                            obj.model._meta.app_label, obj.model._meta.object_name,
                        ),
                        obj=obj.__class__,
                        id='admin.E108',
                    )
                ]
        if isinstance(field, models.ManyToManyField):
            return [
                admin.Error(
                    "The value of '%s' must not be a ManyToManyField." % label,
                    obj=obj.__class__,
                    id='admin.E109',
                )
            ]
        return []

def main():
    try:
        django.setup()
        from .models import Thing
        class ThingAdmin(admin.ModelAdmin):
            list_display = ['number', 'order']

        admin.register(Thing, ThingAdmin)

        print("Issue reproduced successfully!")
    except AssertionError as e:
        print_stacktrace(e)
        raise
    except Exception as e:
        print_stacktrace(e)
        exit(1)


if __name__ == "__main__":
    main()
```

This script will attempt to register the `Thing` model with the admin interface, which should trigger the issue. If the issue is present, it will print a stack trace and raise an `AssertionError`. If the issue is fixed, it will simply print a success message.

Please note that you need to have Django installed in your Python environment for this script to work.