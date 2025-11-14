Here is the reproducer script:

```python
import django
from django.contrib import admin
from django.db import models
from django.forms.models import ModelForm, fields
from django.forms.utils import ValidationError

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

def main():
    django.setup()

    class Thing(models.Model):
        pass

    class RelatedModel(models.Model):
        thing = models.ForeignKey(Thing, on_delete=models.CASCADE)
        plop = fields.ArrayField(
            models.CharField(max_length=42),
            default=list,
        )

    class RelatedModelForm(ModelForm):
        def clean(self):
            raise ValidationError("whatever")

    class RelatedModelInline(admin.TabularInline):
        form = RelatedModelForm
        model = RelatedModel
        extra = 1

    admin.site.register(Thing, ThingAdmin=type('ThingAdmin', (admin.ModelAdmin,), {'inlines': [RelatedModelInline]}))

    try:
        thing = Thing()
        thing.save()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")

if __name__ == "__main__":
    main()
```

This script sets up a Django project, defines the models and forms, registers the model with the admin site, and then tries to save an instance of the `Thing` model. If the issue is present, it prints the stack trace and raises an `AssertionError`.