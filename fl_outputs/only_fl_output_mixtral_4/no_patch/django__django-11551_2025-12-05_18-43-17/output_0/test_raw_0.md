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

class PositionField(models.Field):
    def get(self, instance):
        if not isinstance(instance, models.Model):
            raise Exception("Cannot get PositionField on class")
        # Implementation of get method for PositionField
        pass

class Thing(models.Model):
    number = models.IntegerField(default=0)
    order = PositionField()

class ThingAdmin(admin.ModelAdmin):
    list_display = ['number', 'order']

def _check_list_display_item_old(self, obj, item, label):
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
                if hasattr(models.base.Model, item):
                    return [Error(
                        "The value of '%s' refers to '%s', which is not a callable, "
                        "an attribute of '%s', or an attribute or method on '%s.%s'." % (
                            label, item, obj.__class__.__name__,
                            obj.model._meta.app_label, obj.model._meta.object_name,
                        ),
                        obj=obj.__class__,
                        id='admin.E108',
                    )]
                else:
                    return [Error(
                        "The value of '%s' refers to '%s', which is not a callable, "
                        "an attribute of '%s', or an attribute of 'ThingAdmin'." % (
                            label, item, obj.__class__.__name__
                        ),
                        obj=obj.__class__,
                        id='admin.E108',
                    )]
        if isinstance(field, ManyToManyField):
            return [Error(
                "The value of '%s' must not be a ManyToManyField." % label,
                obj=obj.__class__,
                id='admin.E109',
            )]
        return []

def _check_list_display_item_new(self, obj, item, label):
    if callable(item):
        return []
    else:
        try:
            field = obj.model._meta.get_field(item)
        except FieldDoesNotExist:
            try:
                field = getattr(obj.model, item)
            except AttributeError:
                return [Error(
                    "The value of '%s' refers to '%s', which is not a callable, "
                    "an attribute of '%s', or an attribute or method on '%s.%s'." % (
                        label, item, obj.__class__.__name__,
                        obj.model._meta.app_label, obj.model._meta.object_name,
                    ),
                    obj=obj.__class__,
                    id='admin.E108',
                )]
        if isinstance(field, ManyToManyField):
            return [Error(
                "The value of '%s' must not be a ManyToManyField." % label,
                obj=obj.__class__,
                id='admin.E109',
            )]
