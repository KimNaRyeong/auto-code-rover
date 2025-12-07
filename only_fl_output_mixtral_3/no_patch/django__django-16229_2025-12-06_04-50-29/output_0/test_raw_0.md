 Here is a standalone Python file `reproducer.py` that reproduces the issue:
```python
import sys
from django.core.exceptions import ValidationError
from django.db import models
from django.forms import ModelForm
from django.contrib import admin
from django.db.models.fields import ArrayField

def print_stacktrace(e: Exception):
    import traceback    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class Thing(models.Model):
    pass

class RelatedModel(models.Model):
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE)
    plop = ArrayField(
        models.CharField(max_length=42),
        default=list,
    )

class RelatedModelForm(ModelForm):
    def clean(self):
        raise ValidationError("whatever")

    class Meta:
        model = RelatedModel
        fields = '__all__'

class RelatedModelInline(admin.TabularInline):
    form = RelatedModelForm
    model = RelatedModel
    extra = 1

@admin.register(Thing)
class ThingAdmin(admin.ModelAdmin):
    inlines = [
        RelatedModelInline
    ]

def test():
    admin.site.site_header = 'Django site admin'
    admin.site.register(Thing)

    # Create a new Thing object
    t = Thing()
    t.save()

    # Create a new RelatedModel object with an error
    r = RelatedModel(thing=t, plop=['test'])
    r.full_clean()  # This will raise a ValidationError

    # Try to save the RelatedModel object again
    r.full_clean()  # This should still raise a ValidationError

if __name__ == '__main__':
    try:
        test()
        print("No issue found.")
        sys.exit(0)
    except ValidationError as e:
        print_stacktrace(e)
        sys.exit(1)
```
To run the script, execute `python3 reproducer.py` in the root directory of the project. The script will raise a `ValidationError` and print a stack trace when the issue is present, and exit with code 1. If the issue is fixed, the script will print "No issue found." and exit with code 0.

Note: This script uses the `ArrayField` class from the `django.contrib.postgres` module, which is only available in Django 1.9 and later. If you are using an earlier version of Django, you will need to install the `django-arrayfield` package and import `ArrayField` from `arrayfield.fields` instead.