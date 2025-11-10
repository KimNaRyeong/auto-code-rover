Here is the reproducer script:

```python
import django
from django.contrib import admin
from django.db import models
from django.forms import forms, ModelForm, ValidationError
from django.forms.models import model_to_dict
from django.utils.text import slugify

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
    try:
        # Create the models
        class Thing(models.Model):
            pass

        class RelatedModel(models.Model):
            thing = models.ForeignKey(Thing, on_delete=models.CASCADE)
            plop = models.CharField(max_length=42)
            plops = models.ArrayField(
                models.CharField(max_length=42),
                default=list,
            )

        # Create the admin
        class RelatedModelForm(forms.ModelForm):
            def clean(self):
                raise ValidationError("whatever")

        class RelatedModelInline(admin.TabularInline):
            form = RelatedModelForm
            model = RelatedModel
            extra = 1

        admin.site.register(Thing, ThingAdmin=type('ThingAdmin', (admin.ModelAdmin,), {}))
        admin.site.register(RelatedModel, RelatedModelInline)

        # Create an instance of the model and add it to the admin
        thing = Thing()
        thing.save()

        # Try to edit the related model inline
        request = django.http.HttpRequest()
        request.method = 'POST'
        request.POST = {'plops': ['test']}
        request.FILES = {}
        form = RelatedModelForm(model_to_dict(RelatedModel()), data=request.POST)
        if not form.is_valid():
            raise AssertionError("Expected the form to be valid")
    except Exception as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()
```

This script creates the models and admin configuration, then tries to edit a related model inline. If the issue is present, it raises an `AssertionError`.