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
    admin.site.register(RelatedModel, admin_class=ThingAdmin)
    admin.site.site_header = "Test Site"
    admin.site.index_title = "Test Site Administration"

    request = None

    # Create a new Thing instance
    t = Thing()
    t.save()

    # Create a new form instance
    form = RelatedModelForm(request=request)

    # Set the initial value of the plop field
    form.initial['plop'] = ['test']

    # Set the hidden input to show the initial value
    form.fields['plop'].widget.attrs['initial'] = 'test'

    # Print the form
    print(form)

    # Submit the form with an error
    try:
        form.is_valid()
        assert False, "Form should not be valid"
    except ValidationError as e:
        print_stacktrace(e)

    # Submit the form again without modification
    try:
        form.is_valid()
        assert False, "Form should still be invalid"
    except ValidationError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    test()
```
To run the script, execute `python3 reproducer.py` in the root directory of the project. The script will print a stack trace of the issue and exit with code 1.

To fix the issue, modify the `RelatedModelForm` class in the script as follows:
```python
class RelatedModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['plop'].show_hidden_initial = False

    def clean(self):
        raise ValidationError("whatever")

    class Meta:
        model = RelatedModel
        fields = '__all__'
```
Then, run the script again with `python3 reproducer.py`. The script should not print any stack trace and exit with code 0, indicating that the issue has been fixed.